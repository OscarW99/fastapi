import pytest


@pytest.mark.parametrize("val1, val2, ans", [
    (3, 4, 7),
    (2, 6, 8),
    (5, 9, 14)
])
def test_example(val1, val2, ans):
    assert func(val1, val2) == ans
