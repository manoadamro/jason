from unittest import mock

import pytest

from jason.api.token import MatchValues, TokenValidationError


def test_match_values():
    with mock.patch(
        "jason.api.token.flask.request",
        mock.Mock(
            headers={"a": True},
            json={"a": True},
            view_args={"a": True},
            args={"a": True},
            form={"a": True},
        ),
    ):
        MatchValues(
            "header:/a", "json:/a", "url:/a", "query:/a", "form:/a", "jwt:/a"
        ).validate({"a": True})


def test_value_doesnt_match():

    with mock.patch(
        "jason.api.token.flask.request", mock.Mock(view_args={"a": True})
    ), pytest.raises(TokenValidationError):
        MatchValues("url:/a", "jwt:/a").validate({"a": False})


def test_value_missing_path():

    with mock.patch(
        "jason.api.token.flask.request", mock.Mock(view_args={"a": True})
    ), pytest.raises(TokenValidationError):
        MatchValues("url:/a", "jwt:/a").validate({})


def test_not_enough_paths():
    with pytest.raises(ValueError):
        MatchValues("url:/a")


def test_value_invalid_path():
    with pytest.raises(ValueError):
        MatchValues("url:/a", "jwt/a")


def test_value_invalid_object():
    with pytest.raises(AttributeError):
        MatchValues("url:/a", "nope:/a")


def test_auto_fix_paths():
    MatchValues("url:a", "jwt:a")
