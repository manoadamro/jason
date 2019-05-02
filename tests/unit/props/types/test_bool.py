import pytest

from jason import props


def test_validates():
    assert props.Bool().load(True)


def test_true_from_string():
    assert props.Bool().load("true") is True


def test_false_from_string():
    assert props.Bool().load("false") is False


def test_allow_strings_is_false():
    with pytest.raises(props.PropertyValidationError):
        assert props.Bool(allow_strings=False).load("false") is False


def test_nullable():
    props.Bool(nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Bool().load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Bool().load("12345")


def test_default():
    assert props.Bool(default=True).load(None) is True
