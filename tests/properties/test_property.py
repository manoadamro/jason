import pytest

from jason.properties import Property, PropertyValidationError


def test_nullable_no_default():
    prop = Property(nullable=True, default=None)
    assert prop.load(None) is None


def test_nullable_with_default():
    prop = Property(nullable=True, default="thing")
    assert prop.load(None) == "thing"


def test_non_nullable_no_default():
    prop = Property(nullable=False, default=None)
    with pytest.raises(PropertyValidationError):
        prop.load(None)


def test_non_nullable_with_default():
    prop = Property(nullable=False, default="thing")
    assert prop.load(None) == "thing"


def test_callable_default():
    prop = Property(nullable=False, default=lambda: "thing")
    assert prop.load(None) == "thing"


def test_wrong_type():
    prop = Property(types=(str,))
    with pytest.raises(PropertyValidationError):
        prop.load(123)


def test_decorator():
    @Property(nullable=False, default=None)
    def my_property(value):
        return value * 2

    assert my_property.load(12) == 24
