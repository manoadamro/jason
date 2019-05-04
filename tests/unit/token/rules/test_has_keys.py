import pytest

from jason import token


def test_validate():
    check = token.HasKeys("a", "b")
    check.validate({"a": True, "b": 123, "c": "thingy"})


def test_fails_to_validate():
    check = token.HasKeys("a", "d")
    with pytest.raises(token.BatchValidationError):
        check.validate({"a": True, "b": 123, "c": "thingy"})
