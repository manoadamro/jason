import pytest

from jason.schema import Bool, PropertyValidationError


def test_true():
    prop = Bool()
    assert prop.load(True) is True


def test_false():
    prop = Bool()
    assert prop.load(False) is False


def test_no_strings():
    prop = Bool(allow_strings=False)
    with pytest.raises(PropertyValidationError):
        prop.load("true")


def test_true_from_string():
    prop = Bool()
    assert prop.load("true") is True


def test_true_from_capitalised_string():
    prop = Bool()
    assert prop.load("TRUE") is True


def test_false_from_string():
    prop = Bool()
    assert prop.load("false") is False


def test_false_from_capitalised_string():
    prop = Bool()
    assert prop.load("FALSE") is False


def test_invalid_string():
    prop = Bool()
    with pytest.raises(PropertyValidationError):
        prop.load("nope")
