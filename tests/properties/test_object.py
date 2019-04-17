import pytest

from jason import properties as props


@pytest.fixture
def model():
    class MyModel(props.Model):
        my_int = props.Int
        my_float = props.Float(nullable=False)
    return MyModel


def test_from_props(model):
    obj = props.Object(props={"my_int": props.Int, "my_float": props.Float})
    data = {"my_int": 123, "my_float": 12.3}
    assert obj.load(data) == data


def test_from_model(model):
    obj = props.Nested(model)
    data = {"my_int": 123, "my_float": 12.3}
    assert obj.load(data) == data


def test_strict(model):
    obj = props.Nested(model, strict=True)
    data = {"my_int": 123, "my_float": 12.3, "nope": True}
    with pytest.raises(props.PropertyValidationError):
        obj.load(data)
