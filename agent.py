import os
import re
from pathlib import Path

import httpx2
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from mcp.client.streamable_http import streamable_http_client
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient


model = BedrockModel(
    model_id=os.environ.get(
        "BEDROCK_MODEL_ID",
        "us.anthropic.claude-haiku-4-5-20251001-v1:0",
    ),
    region_name=(
        os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION", "us-west-2")
    ),
)

app = BedrockAgentCoreApp()

PROMPTS_DIR = Path(__file__).parent / "prompts"

SYSTEM_PROMPT = "\n\n".join(
    prompt_file.read_text(encoding="utf-8")
    for prompt_file in sorted(PROMPTS_DIR.glob("*.md"))
)


# Bronto MCP gives the agent telemetry / investigation tools.
bronto = MCPClient(
    lambda: streamable_http_client(
        os.environ.get(
            "BRONTO_MCP_URL",
            "https://mcp.eu.bronto.io/mcp",
        ),
        http_client=httpx2.AsyncClient(
            headers={
                "X-BRONTO-API-KEY": os.environ["BRONTO_API_KEY"]
            },
            timeout=60,
        ),
    )
)


def answer(result, reasoning: bool = False) -> str:
    text = str(result).strip()

    if reasoning or not text.startswith("<reasoning>"):
        return text

    if re.search(r"</(reasoning|analysis)>?", text):
        return re.sub(
            r"(?s)^.*</(reasoning|analysis)>?",
            "",
            text,
        ).strip()

    match = re.search(r"(?m)^(\*\*|#|\|)", text)

    return text[match.start():].strip() if match else text


@app.entrypoint
def invoke(payload: dict) -> dict:
    question = payload.get("prompt", "")
    reasoning = bool(payload.get("reasoning", False))

    if not isinstance(question, str) or not question.strip():
        return {
            "error": "'prompt' must be a non-empty string."
        }

    agent = Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[bronto],
    )

    result = agent(question)

    return {
        "result": answer(result, reasoning)
    }


if __name__ == "__main__":
    app.run()
