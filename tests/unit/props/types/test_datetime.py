import datetime

import pytest

from jason import props


def test_validates():
    assert (
        props.Datetime().load(datetime.datetime.fromisoformat("1970-01-01")).isoformat()
        == "1970-01-01T00:00:00+00:00"
    )


def test_from_string():
    assert (
        props.Datetime().load("1970-01-01").isoformat() == "1970-01-01T00:00:00+00:00"
    )


def test_from_string_with_z():
    assert (
        props.Datetime().load("1970-01-01T00:00:00.000Z").isoformat()
        == "1970-01-01T00:00:00+00:00"
    )


def test_from_invalid_string():
    with pytest.raises(props.PropertyValidationError):
        props.Datetime().load("nope")


def test_allow_strings_is_false():
    with pytest.raises(props.PropertyValidationError):
        props.Datetime(allow_strings=False).load("1970-01-01")


def test_nullable():
    props.Datetime(nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Datetime().load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Datetime().load(12345)


def test_default():
    assert props.Datetime(default="1970-01-01").load(None).isoformat()
