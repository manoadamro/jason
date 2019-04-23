from unittest import mock

import pytest

from jason.api import token


@token.token_protect(
    token.HasScopes("some:scope", "some:other"),
    token.MatchValues("token:user_id", "url:user_id"),
)
def some_route():
    return True


def test_protect():
    with mock.patch(
        "jason.api.token.flask.request", mock.Mock(view_args={"user_id": "123"})
    ), mock.patch(
        "jason.api.token.flask.g",
        {"_ACCESS_TOKEN": {"user_id": "123", "scp": ["some:scope", "some:other"]}},
    ):
        assert some_route() is True


def test_fail():
    with mock.patch(
        "jason.api.token.flask.request", mock.Mock(view_args={"user_id": "123"})
    ), mock.patch(
        "jason.api.token.flask.g",
        {"_ACCESS_TOKEN": {"user_id": "123", "scp": ["some:scope"]}},
    ), pytest.raises(
        token.TokenValidationError
    ):
        assert some_route() is True
