import pytest

from jason import token


def test_validate(prop):
    token.AllOf(prop, prop, prop).validate({})


def test_fails_to_validate(prop, err):
    with pytest.raises(token.BatchValidationError):
        token.AllOf(prop, err, prop).validate({})
