from unittest import mock

import pytest

from jason.token import AnyOf, TokenValidationError


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
    AnyOf(false, false, true).validate("token")


def test_all_of_fails(true, false):
    with pytest.raises(TokenValidationError):
        AnyOf(false, false, false).validate("token")
