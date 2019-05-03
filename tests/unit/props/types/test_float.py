import pytest

from jason import props


def test_validate():
    props.Float().load(5)


def test_casts_to_float():
    assert isinstance(props.Float().load(5), float)


def test_loads_int_from_string():
    assert props.Float().load("5") == 5.0


def test_loads_float_from_string():
    assert props.Float().load("5.5") == 5.5


def test_not_allow_strings():
    with pytest.raises(props.PropertyValidationError):
        assert props.Float(allow_strings=False).load("5") == 5.0


def test_accepts_int():
    assert props.Float().load(5) == 5.0


def test_accepts_float():
    assert props.Float().load(5.5) == 5.5


def test_too_low():
    with pytest.raises(props.PropertyValidationError):
        props.Float(min_value=10).load(5)


def test_too_high():
    with pytest.raises(props.PropertyValidationError):
        props.Float(max_value=10).load(20)


def test_nullable():
    props.Float(nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Float().load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Float().load("nope")


def test_default():
    assert props.Float(default=123).load(None) == 123
