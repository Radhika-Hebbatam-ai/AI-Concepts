from typing import Any

from langchain.agents import create_agent
from langchain_core.language_models import BaseChatModel
from langgraph.checkpoint.memory import InMemorySaver

from agent_core.domain.tools import multiply

SYSTEM_PROMPT = (
    "You are a helpful assistant. You cannot do arithmetic yourself. "
    "For ANY multiplication, you MUST call the multiply tool and use its result."
)


def build_agent(llm: BaseChatModel) -> Any:
    return create_agent(
        model=llm,
        tools=[multiply],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=InMemorySaver(),
    )
