import pytest

from jason import token


def test_validate():
    check = token.HasScopes("read:thing", "write:thing")
    check.validate({"scp": ["read:thing", "write:thing"]})


def test_fails_to_validate():
    check = token.HasScopes("read:thing", "write:thing")
    with pytest.raises(token.BatchValidationError):
        check.validate({"scp": ["read:other", "write:other"]})
