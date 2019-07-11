from unittest import mock

import pytest

from jason import token


def test_match_values():
    with mock.patch(
        "flask.request",
        mock.Mock(
            headers={"a": True},
            json={"a": True},
            view_args={"a": True},
            args={"a": True},
            form={"a": True},
        ),
    ):
        token.MatchValues(
            "header:/a", "json:/a", "url:/a", "query:/a", "form:/a", "token:/a"
        ).validate({"a": True})


def test_value_doesnt_match():
    with mock.patch("flask.request", mock.Mock(view_args={"a": True})), pytest.raises(
        token.TokenValidationError
    ):
        token.MatchValues("url:/a", "token:/a").validate({"a": False})


def test_value_missing_path():
    with mock.patch("flask.request", mock.Mock(view_args={"a": True})), pytest.raises(
        token.TokenValidationError
    ):
        token.MatchValues("url:/a", "token:/a").validate({})


def test_not_enough_paths():
    with pytest.raises(ValueError):
        token.MatchValues("url:/a")


def test_value_invalid_path():
    with pytest.raises(ValueError):
        token.MatchValues("url:/a", "token/a")


def test_value_invalid_object():
    with pytest.raises(AttributeError):
        token.MatchValues("url:/a", "nope:/a")


def test_auto_fix_paths():
    token.MatchValues("url:a", "token:a")
