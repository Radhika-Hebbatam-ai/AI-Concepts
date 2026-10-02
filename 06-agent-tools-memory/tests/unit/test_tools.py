import pytest

from agent_core.domain.tools import multiply


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (4837, 219, 1059303),  # large numbers (LLMs get these wrong)
        (-3, 4, -12),  # negative
        (-3, -4, 12),  # two negatives
        (0, 999, 0),  # zero
    ],
)
def test_multiply_returns_product(a: float, b: float, expected: float) -> None:
    assert multiply(a, b) == expected


def test_multiply_handles_decimals() -> None:
    assert multiply(0.1, 3) == pytest.approx(0.3)
