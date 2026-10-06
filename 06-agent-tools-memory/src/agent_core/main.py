import time
import uuid

import structlog

from agent_core.config import Settings
from agent_core.infrastructure.agent import build_agent
from agent_core.infrastructure.llm import create_chat_model
from agent_core.observability.logging import configure_logging, get_logger, log_tool_calls


def main() -> None:
    settings = Settings()  # type: ignore[call-arg]
    configure_logging(settings.log_level)
    logger = get_logger()
    llm = create_chat_model(settings)
    agent = build_agent(llm)
    session_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(session_id=session_id)
    config = {"configurable": {"thread_id": session_id}}

    print("Ask a question (type 'exit' to quit)")
    while True:
        question = input("You: ").strip()
        if question.lower() == "exit":
            break

        start = time.perf_counter()
        result = agent.invoke({"messages": [{"role": "user", "content": question}]}, config=config)
        latency_ms = round((time.perf_counter() - start) * 1000)

        answer = result["messages"][-1].content
        log_tool_calls(result["messages"])
        logger.info("agent_called", model=settings.groq_model, latency_ms=latency_ms)
        print(f"AI: {answer}")


if __name__ == "__main__":
    main()
