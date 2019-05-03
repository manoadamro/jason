import pytest

from jason import props


def test_validates():
    props.Regex("[az]+").load("abc")


def test_nullable():
    props.Regex("[az]+", nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Regex("[az]+").load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Regex("[az]+").load(12345)


def test_invalid_string():
    with pytest.raises(props.PropertyValidationError):
        props.Regex("[az]+").load("ABC")


def test_default():
    assert props.Regex("[az]+", default="abcde").load(None) == "abcde"
