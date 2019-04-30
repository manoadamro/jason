import pytest

from jason.props import Number, PropertyValidationError


def test_value_too_low():
    prop = Number(min_value=10, max_value=20)
    with pytest.raises(PropertyValidationError):
        prop.load(5)


def test_value_too_high():
    prop = Number(min_value=10, max_value=20)
    with pytest.raises(PropertyValidationError):
        prop.load(25)


def test_no_min():
    prop = Number(min_value=None, max_value=20)
    assert prop.load(5) == 5


def test_no_max():
    prop = Number(min_value=10, max_value=None)
    assert prop.load(25) == 25


def test_no_range():
    prop = Number(min_value=None, max_value=None)
    assert prop.load(5) == 5


def test_float_from_string():
    prop = Number(allow_strings=True)
    assert prop.load("12.5") == 12.5


def test_int_from_string():
    prop = Number(allow_strings=True)
    assert prop.load("12") == 12


def test_string_float_when_strings_not_allowed():
    prop = Number(allow_strings=False)
    with pytest.raises(PropertyValidationError):
        prop.load("12.5")


def test_string_int_when_strings_not_allowed():
    prop = Number(allow_strings=False)
    with pytest.raises(PropertyValidationError):
        prop.load("12")


def test_invalid_number_from_string():
    prop = Number(allow_strings=True)
    with pytest.raises(PropertyValidationError):
        prop.load("12.34.45")


def test_nan_from_string():
    prop = Number(allow_strings=True)
    with pytest.raises(PropertyValidationError):
        prop.load("nope")
