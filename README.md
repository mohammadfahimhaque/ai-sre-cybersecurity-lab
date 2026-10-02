<p align="center">
  <img src="assets/hero-banner.png" alt="Cybersecurity Research Agent" width="100%" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-111111?style=flat-square" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/Amazon-Bedrock-111111?style=flat-square" alt="Amazon Bedrock" />
  <img src="https://img.shields.io/badge/Agent-Strands-111111?style=flat-square" alt="Strands Agents" />
  <img src="https://img.shields.io/badge/Protocol-MCP-111111?style=flat-square" alt="MCP" />
  <img src="https://img.shields.io/badge/Runtime-Docker-111111?style=flat-square" alt="Docker" />
</p>

<p align="center">
  <strong>Evidence-grounded cybersecurity investigation with telemetry, source-code context, and AI-assisted analysis.</strong>
</p>

---

## Overview

The **Cybersecurity Research Agent** is an AI-assisted investigation system designed to analyze security evidence while remaining explicit about what it can — and cannot — verify.

Its core principle is simple:

> **Evidence first. Conclusions second.**

The agent can:

- investigate telemetry through **Bronto MCP**
- inspect repository source code through **GitHub MCP in read-only mode**
- correlate security-relevant events
- distinguish verified evidence from hypotheses
- state confidence and investigation limitations
- publish structured findings as **GitHub Issues**

The project combines cybersecurity investigation methodology with AI agent engineering, cloud infrastructure, MCP-based tool integration, and security-conscious system design.

---

## Architecture

<p align="center">
  <img src="assets/architecture-overview.png" alt="Cybersecurity Research Agent architecture" width="100%" />
</p>

The system is built around a small number of clearly separated components.

| Layer | Responsibility |
|---|---|
| **Bedrock AgentCore** | Hosts the agent invocation runtime |
| **Strands Agent** | Orchestrates the model and connected tools |
| **Amazon Bedrock** | Provides the foundation model |
| **Bronto MCP** | Provides telemetry search and investigation data |
| **GitHub MCP** | Provides read-only repository inspection |
| **GitHub REST API** | Publishes the final investigation report |

The current default Bedrock model is:

```text
us.anthropic.claude-haiku-4-5-20251001-v1:0
```

The model can be changed at runtime using:

```text
BEDROCK_MODEL_ID
```

---

## Investigation Workflow

<p align="center">
  <img src="assets/investigation-workflow.png" alt="Cybersecurity investigation workflow" width="100%" />
</p>

The agent follows an evidence-first investigation process.

### 01 — Collect Context

Establish:

- investigation question
- scope
- relevant timeframe
- available evidence
- available tools

### 02 — Search Telemetry

Use Bronto MCP to query available:

- datasets
- events
- authentication activity
- application logs
- security-relevant signals

### 03 — Correlate Evidence

Compare available indicators such as:

- timestamps
- users
- IP addresses
- services
- event sequences
- processes
- related identifiers

### 04 — Inspect Source Code

When repository context is relevant, GitHub MCP can inspect committed source code in **read-only mode**.

### 05 — Report Findings

The final investigation is structured around:

- observation
- verified evidence
- interpretation
- limitations
- next investigation step
- confidence level

---

## Evidence Model

The agent is explicitly instructed to separate facts from hypotheses.

```text
Tool result        → Evidence
Evidence pattern   → Observation
Observation        → Supported interpretation
Missing evidence   → Limitation
Unsupported claim  → Not allowed
```

> **Tool results are evidence. Assumptions are not evidence.**

This distinction is one of the core design principles of the project.

---

## Capabilities

### Telemetry Investigation

Through Bronto MCP, the agent can:

- discover available telemetry
- search log data
- retrieve matching events
- correlate related activity
- inspect timestamps and structured fields
- compare event sequences
- support findings using returned evidence

### Repository Investigation

Through GitHub MCP, the agent can:

- inspect repository files
- read source code
- examine project configuration
- gather repository context relevant to an investigation

The GitHub MCP connection is configured with:

```text
X-MCP-Toolsets: repos
X-MCP-Readonly: true
```

This keeps repository inspection separate from write operations.

### Structured Reporting

After an investigation is completed, the result can be published as a GitHub issue containing:

- finding
- verified evidence
- confidence
- limitations
- recommended next step

---

## Capability Boundaries

The agent is deliberately instructed not to claim capabilities it does not have.

It must not invent:

- vulnerabilities
- indicators of compromise
- malware findings
- attack paths
- IP reputation
- IP geolocation
- threat-intelligence results
- account compromise
- exploitation
- scan results
- telemetry that was never returned by a tool

If the required evidence or integration is unavailable, the expected behavior is to state that limitation clearly.

> **Missing evidence is a finding too.**

---

## Security Design

Security boundaries are part of the architecture rather than an afterthought.

| Control | Implementation |
|---|---|
| **Secret isolation** | Runtime secrets are supplied through environment variables |
| **Git protection** | `.env` is excluded from version control |
| **Read-only source inspection** | GitHub MCP uses read-only mode |
| **Tool restriction** | GitHub MCP requests the `repos` toolset |
| **Separate write path** | GitHub issue creation uses an explicit REST request |
| **Evidence discipline** | Prompts distinguish verified facts from hypotheses |
| **Capability disclosure** | Missing tools and evidence must be stated |
| **Output cleanup** | Leading reasoning-style tags are removed from normal output |

### Secret Handling

```text
.env           → real local configuration
.env.example   → safe configuration template
```

Real API keys, access tokens, and credentials should never be committed.

---

## Prompt Architecture

Agent behavior is split across focused prompt modules rather than one large system prompt.

```text
prompts/
├── capabilities.md
├── my.md
├── report.md
├── role.md
└── rules.md
```

| File | Responsibility |
|---|---|
| `role.md` | Defines the cybersecurity research-assistant role |
| `rules.md` | Defines evidence and hallucination boundaries |
| `my.md` | Defines investigation methodology |
| `report.md` | Defines investigation-report structure |
| `capabilities.md` | Defines available capabilities and limitations |

At startup, these files are loaded and combined into the agent system prompt.

---

## Example Investigation

During development, synthetic authentication telemetry was introduced to test the investigation workflow.

```text
00:44:24.033  failed login
00:44:24.156  failed login
00:44:24.503  successful login
```

The events shared the same test user and source IP.

The agent was able to:

```text
Collect telemetry
       ↓
Correlate timestamps + user + IP
       ↓
Identify failed → failed → success
       ↓
Separate evidence from hypotheses
       ↓
Identify missing context
       ↓
Assign confidence
       ↓
Publish investigation report
```

The important outcome was not simply identifying a suspicious event sequence.

The agent also recognized that the available evidence was **insufficient to prove compromise**.

That distinction is central to the project.

---

## Model Evaluation

The same investigation workflow was tested with two Amazon Bedrock models.

### Claude Haiku 4.5

During the project test, Claude successfully:

- retrieved the synthetic telemetry
- reconstructed the event sequence
- correlated evidence
- respected capability boundaries
- produced a structured investigation report

### Amazon Nova Lite

Nova Lite was tested using the same investigation prompt.

In that specific test, it did not retrieve the known telemetry successfully.

The comparison highlighted an important agent-engineering principle:

> Model evaluation should measure **tool-use reliability**, not only natural-language output quality.

Claude Haiku 4.5 remains the current default model for this project.

---

## Tech Stack

| Area | Technology |
|---|---|
| **Language** | Python 3.12 |
| **Foundation Model** | Anthropic Claude Haiku 4.5 |
| **Model Evaluation** | Amazon Nova Lite |
| **Model Platform** | Amazon Bedrock |
| **Runtime** | Amazon Bedrock AgentCore |
| **Agent Framework** | Strands Agents |
| **Tool Protocol** | Model Context Protocol |
| **Telemetry** | Bronto MCP |
| **Repository Context** | GitHub MCP |
| **Reporting** | GitHub REST API / Issues |
| **Containerization** | Docker |
| **Cloud** | AWS |
| **Source Control** | Git / GitHub |

---

## Project Structure

```text
.
├── assets/
│   ├── architecture-overview.png
│   ├── hero-banner.png
│   └── investigation-workflow.png
│
├── prompts/
│   ├── capabilities.md
│   ├── my.md
│   ├── report.md
│   ├── role.md
│   └── rules.md
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── agent.py
└── requirements.txt
```

---

## Local Setup

### 1. Clone the Repository

```bash
git clone git@github.com:mohammadfahimhaque/ai-sre-cybersecurity-lab.git
cd ai-sre-cybersecurity-lab
```

### 2. Prepare Configuration

```bash
cp .env.example .env
```

Example:

```env
AWS_DEFAULT_REGION=us-west-2
BEDROCK_MODEL_ID=us.anthropic.claude-haiku-4-5-20251001-v1:0

BRONTO_MCP_URL=https://mcp.eu.bronto.io/mcp
BRONTO_API_KEY=your_bronto_api_key_here

GITHUB_REPOSITORY=mohammadfahimhaque/ai-sre-cybersecurity-lab
```

Never commit the real `.env` file.

### 3. Authenticate AWS

```bash
aws login --remote
```

Verify the active AWS identity:

```bash
aws sts get-caller-identity
```

### 4. Build the Docker Image

```bash
docker build -t ai-sre-agent .
```

### 5. Run the Agent

```bash
docker run --rm --name ai-sre-agent-test \
  -p 8080:8080 \
  --env-file .env \
  -v "$HOME/.aws:/root/.aws" \
  -e AWS_PROFILE=default \
  -e GITHUB_TOKEN="$(gh auth token)" \
  ai-sre-agent
```

---

## API Usage

Send an investigation request:

```bash
curl http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "prompt":
    "Investigate the available security telemetry and report only evidence supported by your connected tools."
  }'
```

The endpoint currently returns the URL of the generated GitHub investigation issue:

```json
{
  "result": "https://github.com/.../issues/..."
}
```

---

## Current Capability Map

| Capability | Status |
|---|:---:|
| Telemetry discovery | ✅ |
| Telemetry search | ✅ |
| Event correlation | ✅ |
| Evidence-based investigation | ✅ |
| Confidence reporting | ✅ |
| GitHub source inspection | ✅ |
| Read-only repository MCP | ✅ |
| GitHub investigation reporting | ✅ |
| Threat intelligence | — |
| IP reputation | — |
| IP geolocation | — |
| EDR telemetry | — |
| Packet inspection | — |
| Vulnerability scanning | — |

Unavailable capabilities are treated as explicit limitations rather than opportunities to invent results.

---

## Development Milestones

```text
01  Bedrock model invocation             ✓
02  Cybersecurity agent identity         ✓
03  Bronto MCP telemetry                 ✓
04  GitHub investigation reporting       ✓
05  Investigation methodology            ✓
06  Capability boundaries                ✓
07  Model comparison                     ✓
08  Read-only GitHub source access       ✓
09  Portfolio redesign                   ✓
```

---

## Roadmap

- [ ] Structured investigation schema
- [ ] Unit tests
- [ ] Integration tests
- [ ] Improved exception handling
- [ ] Investigation severity classification
- [ ] Synthetic security-scenario test suite
- [ ] Safer output sanitization
- [ ] Threat-intelligence integration
- [ ] Additional telemetry sources
- [ ] Alert-to-code correlation
- [ ] Analyst-facing web interface
- [ ] Cloud deployment
- [ ] Agent evaluation framework

---

## Design Philosophy

This project sits at the intersection of:

```text
Cybersecurity
      ×
AI Agent Engineering
      ×
Cloud Infrastructure
      ×
Product & UX Thinking
```

The goal is not to build an AI system that always produces an answer.

The goal is to build an investigation system that understands:

> **what it knows, what it does not know, and what evidence is needed next.**

---

## Author

**Mohammad Fahim Haque**
MSc Computing (Cybersecurity) — Dublin City University

Software development · Cybersecurity · AI systems · UI/UX design

[GitHub](https://github.com/mohammadfahimhaque)

---

<p align="center">
  <strong>Evidence before conclusions.</strong>
</p>
