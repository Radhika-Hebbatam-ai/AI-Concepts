import json

import pytest

from agent_core.observability.logging import configure_logging, get_logger


def test_logs_are_json_with_context(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(level="INFO")

    get_logger().info("tool_called", tool="multiply")

    line = capsys.readouterr().out.strip()
    data = json.loads(line)
    assert data["event"] == "tool_called"
    assert data["tool"] == "multiply"
    assert data["level"] == "info"
    assert "timestamp" in data


def test_debug_is_hidden_at_info_level(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(level="INFO")

    get_logger().debug("noisy detail")

    assert capsys.readouterr().out == ""
