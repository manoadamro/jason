import pytest

from jason.schema import Array, PropertyValidationError, String


def test_value_too_short():
    prop = Array(String(), min_length=10, max_length=20)
    with pytest.raises(PropertyValidationError):
        prop.load(["a"] * 5)


def test_value_too_long():
    prop = Array(String, min_length=10, max_length=20)
    with pytest.raises(PropertyValidationError):
        prop.load(["a"] * 25)


def test_no_min():
    prop = Array(String(), min_length=None, max_length=20)
    assert prop.load(["a"] * 5) == ["a"] * 5


def test_no_max():
    prop = Array(String(), min_length=10, max_length=None)
    assert prop.load(["a"] * 25) == ["a"] * 25


def test_no_range():
    prop = Array(String(), min_length=None, max_length=None)
    assert prop.load(["a"] * 5) == ["a"] * 5


def test_prop_is_type():
    prop = Array(String)
    assert prop.load(["a"] * 5) == ["a"] * 5


def test_validates_array():
    prop = Array(String)
    assert prop.load(["a"] * 5) == ["a"] * 5


def test_invalidates_array():
    prop = Array(String)
    with pytest.raises(PropertyValidationError):
        prop.load([1])
