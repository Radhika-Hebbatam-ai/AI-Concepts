from agent_core.domain.tools import multiply


def test_multiply_returns_product() -> None:
    assert multiply(4837, 219) == 1059303
