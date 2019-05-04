from unittest import mock

import pytest

from jason import token


@pytest.fixture
def prop():
    prop = mock.Mock()
    prop.validate.side_effect = lambda x: x
    return prop


@pytest.fixture
def err():
    def _err():
        raise token.TokenValidationError("error")

    prop = mock.Mock()
    prop.validate.side_effect = lambda x: _err()
    return prop


def test_validate(prop, err):
    token.NoneOf(err, err, err).validate({})


def test_fails_to_validate(prop, err):
    with pytest.raises(token.TokenValidationError):
        token.NoneOf(err, err, prop).validate({})
