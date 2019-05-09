import pytest

from jason import token


def test_validate(prop, err):
    token.NoneOf(err, err, err).validate({})


def test_fails_to_validate(prop, err):
    with pytest.raises(token.TokenValidationError):
        token.NoneOf(err, err, prop).validate({})
