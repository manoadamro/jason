import pytest

from jason.core.schema import AnyOf, Float, Int, PropertyValidationError, String


def test_validates():
    rule = AnyOf(Int, String)
    assert rule.load("something") == "something"
    assert rule.load(123) == 123


def test_fails_invalidates():
    rule = AnyOf(Int, Float)
    with pytest.raises(PropertyValidationError):
        rule.load(True)
