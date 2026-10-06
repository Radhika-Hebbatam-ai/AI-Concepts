import logging
from typing import Any

import structlog


def configure_logging(level: str = "INFO") -> None:
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelNamesMapping()[level]),
    )


def get_logger() -> Any:
    return structlog.get_logger()


def log_tool_calls(messages: list[Any]) -> None:
    logger = get_logger()
    for message in messages:
        for call in getattr(message, "tool_calls", None) or []:
            logger.info("tool_called", tool=call["name"], args=call["args"])
        if type(message).__name__ == "ToolMessage":
            logger.info("tool_result", tool=message.name, result=message.content)
