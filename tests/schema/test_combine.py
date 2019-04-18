import pytest
from jason.schema import (
    Bool,
    Combine,
    Float,
    Inline,
    Int,
    Model,
    Nested,
    PropertyValidationError,
    String,
)


@pytest.fixture
def model():
    class MyModel(Model):
        my_int = Int
        my_float = Float

    return MyModel


@pytest.fixture
def inline():
    return Inline(props=dict(my_string=String))


@pytest.fixture
def nested():
    class NestedModel(Model):
        my_bool = Bool

    return Nested(NestedModel)


def test_combine(model, inline, nested):
    combined = Combine(model, inline, nested, {"my_thing": Int})
    actual = list(sorted(combined.props.keys()))
    expected = list(sorted(("my_int", "my_float", "my_string", "my_bool", "my_thing")))
    assert expected == actual


def test_duplicate_key(inline):
    with pytest.raises(PropertyValidationError):
        Combine(inline, {"my_string": Int})


def test_wrong_type(inline):
    with pytest.raises(ValueError):
        Combine(inline, True)


def test_invalid_property_type(inline):
    with pytest.raises(PropertyValidationError):
        Combine(inline, {"my_string": True})
