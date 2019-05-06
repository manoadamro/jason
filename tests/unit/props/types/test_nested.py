import pytest

from jason import props


class MyModel(props.Model):
    x = props.Int


def test_nullable():
    props.Nested(MyModel, nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Nested(MyModel).load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Nested(MyModel).load("12345")


def test_default():
    assert props.Nested(MyModel, default={"x": 123}).load(None) == {"x": 123}


def test_collects_errors():
    with pytest.raises(props.BatchValidationError):
        props.Nested(MyModel).load({"y": "nope"})
