from unittest import mock

import pytest

from jason.api.token import HasValue, TokenValidationError


def test_has_value():
    HasValue("/a", True).validate({"a": True})


def test_autofix_pointer():
    HasValue("a", True).validate({"a": True})


def test_missing_key():
    with pytest.raises(TokenValidationError):
        HasValue("/a", True).validate({"a": False})


def test_has_value_fails():
    with pytest.raises(TokenValidationError):
        HasValue("/a", True).validate({"b": True})
