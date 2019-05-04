from unittest import mock

import pytest

from jason import props, token


@pytest.fixture
def prop():
    prop = mock.Mock()
    prop.validate.side_effect = lambda x: x
    return prop


@pytest.fixture
def err():
    def _err():
        raise props.BatchValidationError("", [])

    prop = mock.Mock()
    prop.validate.side_effect = lambda x: _err()
    return prop


@mock.patch("flask.g", {"_ACCESS_TOKEN": "token"})
def test_validate(prop):
    @token.protect(prop, prop, prop)
    def protected():
        return True

    assert protected() is True


@mock.patch("flask.g", {"_ACCESS_TOKEN": "token"})
def test_fails_to_validate(prop, err):
    @token.protect(prop, prop, err)
    def protected():
        return True

    with pytest.raises(props.BatchValidationError):
        protected()
