from typing import Any

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage

from agent_core.infrastructure.agent import build_agent


class FakeLLM(GenericFakeChatModel):
    def bind_tools(self, tools: Any, **kwargs: Any) -> "FakeLLM":
        return self


def test_agent_calls_multiply_tool() -> None:
    llm = FakeLLM(
        messages=iter(
            [
                AIMessage(
                    content="",
                    tool_calls=[{"name": "multiply", "args": {"a": 4837, "b": 219}, "id": "1"}],
                ),
                AIMessage(content="The answer is 1059303"),
            ]
        )
    )
    agent = build_agent(llm)

    result = agent.invoke({"messages": [{"role": "user", "content": "What is 4837 * 219?"}]})

    assert result["messages"][2].content == "1059303.0"
    assert result["messages"][-1].content == "The answer is 1059303"
