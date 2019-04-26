from unittest import mock

import pytest

from jason.token import HasKeys, TokenValidationError


def test_has_keys():
    HasKeys("a", "b", "c").validate({"a": True, "b": True, "c": True})


def test_has_keys_fails():
    with pytest.raises(TokenValidationError):
        HasKeys("a", "b", "c").validate({"a": True, "b": True, "d": True})
