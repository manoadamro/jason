import pytest

from jason import props


class ModelA(props.Model):
    x = props.Int()


class ModelB(props.Model):
    y = props.Int


def test_combine():
    assert list(props.Compound(ModelA, ModelB).__props__.keys()) == ["x", "y"]


def test_combine_inline():
    prop = props.Compound(ModelA, props.Inline(props=dict(y=props.Int)))
    assert list(prop.__props__.keys()) == ["x", "y"]


def test_combine_dict():
    prop = props.Compound(ModelA, {"y": props.Int})
    assert list(prop.__props__.keys()) == ["x", "y"]


def test_combine_nested():
    prop = props.Compound(ModelA, props.Nested(ModelB))
    assert list(prop.__props__.keys()) == ["x", "y"]


def test_combine_invalid():
    with pytest.raises(ValueError):
        props.Compound(ModelA, 123)


def test_combine_invalid_props():
    with pytest.raises(ValueError):
        props.Compound(ModelA, {"x": 123})


def test_nullable():
    props.Compound(ModelA, ModelB, nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Compound(ModelA, ModelB).load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Compound(ModelA, ModelB).load("12345")


def test_default():
    prop = props.Compound(ModelA, ModelB, default={"x": 1, "y": 2})
    assert prop.load(None) == {"x": 1, "y": 2}


def test_write_identical_items():
    class ModelA(props.Model):
        x = props.Int(min_value=5, max_value=10)

    class ModelB(props.Model):
        x = props.Int(min_value=5, max_value=10)

    props.Compound(ModelA, ModelB)


def test_fails_to_write_non_identical_items():
    class ModelA(props.Model):
        x = props.Int(min_value=5, max_value=10)

    class ModelB(props.Model):
        x = props.Int(min_value=5, max_value=11)

    with pytest.raises(ValueError):
        props.Compound(ModelA, ModelB)


def test_fails_to_combine_wrong_types():
    class ModelA(props.Model):
        x = props.Int()

    class ModelB(props.Model):
        x = props.String()

    with pytest.raises(ValueError):
        props.Compound(ModelA, ModelB)
