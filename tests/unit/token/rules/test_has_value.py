import pytest

from jason import props, token


def test_validate():
    token.HasValue("user/id", 123).validate({"user": {"id": 123}})


def test_validate_property():
    token.HasValue("user/id", props.Int).validate({"user": {"id": 123}})


def test_fails_to_validate():
    with pytest.raises(token.TokenValidationError):
        token.HasValue("user/id", 123).validate({"user": {"id": 456}})


def test_fails_to_validate_missing_value():
    with pytest.raises(token.TokenValidationError):
        token.HasValue("user/id", 123).validate({"user": {"nope": True}})
