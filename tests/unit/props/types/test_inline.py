import pytest

from jason import props


def test_nullable():
    props.Inline(props={}, nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Inline(props={}).load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Inline(props={}).load("12345")


def test_default():
    assert props.Inline(props={"x": props.Int}, default={"x": 123}).load(None) == {
        "x": 123
    }
