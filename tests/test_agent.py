import os
from unittest.mock import Mock, patch

import pytest

import agent


def test_get_question_accepts_valid_prompt():
    assert agent.get_question(
        {"prompt": "  Investigate suspicious login activity  "}
    ) == "Investigate suspicious login activity"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"prompt": ""},
        {"prompt": "   "},
        {"prompt": None},
        {"prompt": 123},
        {"prompt": []},
    ],
)
def test_get_question_rejects_invalid_prompt(payload):
    assert agent.get_question(payload) is None


@pytest.mark.parametrize(
    "tag",
    ["reasoning", "analysis", "thinking"],
)
def test_answer_removes_leading_reasoning_blocks(tag):
    result = (
        f"<{tag}>internal reasoning should not be returned</{tag}>\n"
        "Verified finding."
    )

    assert agent.answer(result) == "Verified finding."


def test_answer_preserves_normal_output():
    result = "Verified evidence with medium confidence."

    assert agent.answer(result) == result


@patch.dict(
    os.environ,
    {
        "GITHUB_REPOSITORY": "example/security-agent",
        "GITHUB_TOKEN": "test-token",
    },
)
@patch("agent.httpx2.post")
def test_file_issue_posts_expected_report(mock_post):
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "html_url": "https://github.com/example/security-agent/issues/1"
    }

    mock_post.return_value = response

    url = agent.file_issue(
        "Investigate login activity",
        "Verified investigation report",
    )

    assert url == "https://github.com/example/security-agent/issues/1"

    mock_post.assert_called_once()

    _, kwargs = mock_post.call_args

    assert kwargs["json"]["body"] == "Verified investigation report"
    assert kwargs["json"]["title"].startswith("[Security investigation]")
    assert kwargs["headers"]["Authorization"] == "Bearer test-token"
