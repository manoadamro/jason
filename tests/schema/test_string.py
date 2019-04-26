import pytest

from jason.schema import PropertyValidationError, String


def test_value_too_short():
    prop = String(min_length=10, max_length=20)
    with pytest.raises(PropertyValidationError):
        prop.load("a" * 5)


def test_value_too_long():
    prop = String(min_length=10, max_length=20)
    with pytest.raises(PropertyValidationError):
        prop.load("a" * 25)


def test_no_min():
    prop = String(min_length=None, max_length=20)
    assert prop.load("a" * 5) == "a" * 5


def test_no_max():
    prop = String(min_length=10, max_length=None)
    assert prop.load("a" * 25) == "a" * 25


def test_no_range():
    prop = String(min_length=None, max_length=None)
    assert prop.load("a" * 5) == "a" * 5
