import pytest

from jason import props


def test_nullable():
    props.String(nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.String().load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Email().load(12345)


def test_default():
    assert props.Email(default="a@b.com").load(None) == "a@b.com"


def test_too_short():
    with pytest.raises(props.PropertyValidationError):
        props.Email(min_length=10).load("123")


def test_too_long():
    with pytest.raises(props.PropertyValidationError):
        props.Email(max_length=2).load("123")
