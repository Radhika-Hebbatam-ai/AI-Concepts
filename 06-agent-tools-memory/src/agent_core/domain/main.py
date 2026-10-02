import time

from agent_core.config import Settings
from agent_core.infrastructure.llm import create_chat_model
from agent_core.observability.logging import configure_logging, get_logger


def main() -> None:
    settings = Settings()  # type: ignore[call-arg]
    configure_logging(settings.log_level)
    logger = get_logger()
    llm = create_chat_model(settings)

    print("Ask a question (type 'exit' to quit)")
    while True:
        question = input("You: ").strip()
        if question.lower() == "exit":
            break

        start = time.perf_counter()
        response = llm.invoke(question)
        latency_ms = round((time.perf_counter() - start) * 1000)

        logger.info("llm_called", model=settings.groq_model, latency_ms=latency_ms)
        print(f"AI: {response.content}")


if __name__ == "__main__":
    main()
