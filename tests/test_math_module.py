import pytest

from math_module import factorial, is_even


def test_factorial():
    assert factorial(5) == 120
    assert factorial(0) == 1
    assert factorial(1) == 1


@pytest.mark.parametrize("n, expected", [(2, 2), (3, 6), (10, 3628800), (20, 2432902008176640000)])
def test_factorial_values(n, expected):
    assert factorial(n) == expected


def test_factorial_negative_raises():
    with pytest.raises(ValueError):
        factorial(-1)


@pytest.mark.parametrize("bad", [2.5, "5", None, True])
def test_factorial_wrong_type_raises(bad):
    with pytest.raises(TypeError):
        factorial(bad)


@pytest.mark.parametrize("n, expected", [(0, True), (1, False), (2, True), (-3, False), (-4, True), (10**12, True)])
def test_is_even(n, expected):
    assert is_even(n) is expected


def test_is_even_wrong_type_raises():
    with pytest.raises(TypeError):
        is_even(3.0)
