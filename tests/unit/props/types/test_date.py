import datetime

import pytest

from jason import props


def test_validates():
    assert (
        props.Date().load(datetime.date.fromisoformat("1970-01-01")).isoformat()
        == "1970-01-01"
    )


def test_true_from_string():
    assert props.Date().load("1970-01-01").isoformat() == "1970-01-01"


def test_from_invalid_string():
    with pytest.raises(props.PropertyValidationError):
        props.Date().load("nope")


def test_allow_strings_is_false():
    with pytest.raises(props.PropertyValidationError):
        props.Date(allow_strings=False).load("1970-01-01")


def test_nullable():
    props.Date(nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Date().load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Date().load(12345)


def test_default():
    assert props.Date(default="1970-01-01").load(None).isoformat()
