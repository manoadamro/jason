import pytest

from jason import props


def test_validate():
    props.Int().load(5)


def test_loads_int_from_string():
    assert props.Int().load("5") == 5


def test_rejects_float_from_string():
    with pytest.raises(props.PropertyValidationError):
        props.Int().load("5.5")


def test_not_allow_strings():
    with pytest.raises(props.PropertyValidationError):
        assert props.Int(allow_strings=False).load("5") == 5


def test_accepts_int():
    assert props.Int().load(5) == 5


def test_rejects_float():
    with pytest.raises(props.PropertyValidationError):
        assert props.Int().load(5.5)


def test_too_low():
    with pytest.raises(props.PropertyValidationError):
        props.Int(min_value=10).load(5)


def test_too_high():
    with pytest.raises(props.PropertyValidationError):
        props.Int(max_value=10).load(20)


def test_nullable():
    props.Int(nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Int().load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Int().load("nope")


def test_default():
    assert props.Int(default=123).load(None) == 123
