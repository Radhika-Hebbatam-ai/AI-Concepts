from langchain_groq import ChatGroq

from agent_core.config import Settings


def create_chat_model(settings: Settings) -> ChatGroq:
    """you are chatbot answer general questions"""
    return ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0,
    )
