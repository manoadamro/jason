from uuid import uuid4

import pytest

from jason import props

uuid = str(uuid4())


def test_validates():
    props.Uuid().load(uuid)


def test_nullable():
    props.Uuid(nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Uuid().load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Uuid().load(12345)


def test_invalid_string():
    with pytest.raises(props.PropertyValidationError):
        props.Uuid().load("ABC")


def test_default():
    assert props.Uuid(default=uuid).load(None) == uuid
