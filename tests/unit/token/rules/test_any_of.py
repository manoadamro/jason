import pytest

from jason import token


def test_validate(prop, err):
    token.AnyOf(prop, err, prop).validate({})


def test_fails_to_validate(prop, err):
    with pytest.raises(token.TokenValidationError):
        token.AnyOf(err, err, err).validate({})
