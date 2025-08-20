import pytest
from src.strings.prefix_function import find_positions_of_query


@pytest.mark.parametrize(
    ("text", "query", "positions"),
    [
        ("abczabcf", "abc", [0, 4]),
        ("abc", "zz", None),
        ("abc", "abca", None),
        ("I always wondered why people say hello, and not 'hello'", "hello", [33, 49]),
    ],
)
def test_find_positions_of_query(
    text: str, query: str, positions: list[int] | None
) -> None:
    assert positions == find_positions_of_query(text=text, query=query)
