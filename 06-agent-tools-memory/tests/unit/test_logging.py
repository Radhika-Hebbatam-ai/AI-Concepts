import json

import pytest
import structlog

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


def test_session_id_added_to_logs(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(level="INFO")
    structlog.contextvars.bind_contextvars(session_id="abc")

    get_logger().info("test_event")

    structlog.contextvars.clear_contextvars()
    data = json.loads(capsys.readouterr().out)
    assert data["session_id"] == "abc"
