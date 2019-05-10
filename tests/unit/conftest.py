from unittest import mock

import pytest

from jason import token


@pytest.fixture
def prop():
    prop = mock.Mock()
    prop.validate.side_effect = lambda x: x
    return prop


@pytest.fixture
def err():
    def _err():
        raise token.TokenValidationError("error")

    prop = mock.Mock()
    prop.validate.side_effect = lambda x: _err()
    return prop
