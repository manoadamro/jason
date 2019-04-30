from unittest import mock

import pytest

from jason.token import HasScopes, TokenValidationError


def test_has_scopes():
    HasScopes("a", "b", "c").validate({"scp": ["a", "b", "c", "d"]})


def test_has_scopes_fails():
    with pytest.raises(TokenValidationError):
        HasScopes("a", "b", "c").validate({"scp": ["a", "b", "d"]})
