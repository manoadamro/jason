import pytest

from jason import props


def test_validate():
    props.Number().load(5)


def test_loads_int_from_string():
    assert props.Number().load("5") == 5


def test_loads_float_from_string():
    assert props.Number().load("5.5") == 5.5


def test_not_allow_strings():
    with pytest.raises(props.PropertyValidationError):
        assert props.Number(allow_strings=False).load("5") == 5


def test_accepts_int():
    assert props.Number().load(5) == 5


def test_accepts_float():
    assert props.Number().load(5.5) == 5.5


def test_too_low():
    with pytest.raises(props.PropertyValidationError):
        props.Number(min_value=10).load(5)


def test_too_high():
    with pytest.raises(props.PropertyValidationError):
        props.Number(max_value=10).load(20)


def test_nullable():
    props.Number(nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Number().load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Number().load("nope")


def test_default():
    assert props.Number(default=123).load(None) == 123
