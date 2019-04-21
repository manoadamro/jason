from unittest import mock

import pytest

from jason.api.token import NoneOf, TokenValidationError


@pytest.fixture
def true():
    return mock.Mock()


def raise_err():
    raise TokenValidationError


@pytest.fixture
def false():
    v = mock.Mock()
    v.validate.side_effect = lambda _: raise_err()
    return v


def test_all_of(true, false):
    NoneOf(false, false, false).validate("token")


def test_all_of_fails(true, false):
    with pytest.raises(TokenValidationError):
        NoneOf(false, false, true).validate("token")
