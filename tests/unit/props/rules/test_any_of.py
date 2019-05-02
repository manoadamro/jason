from unittest import mock

import pytest

from jason import props


@pytest.fixture
def prop():
    prop = mock.Mock()
    prop.load.side_effect = lambda x: x
    return prop


@pytest.fixture
def err():
    def _err():
        raise props.PropertyValidationError

    prop = mock.Mock()
    prop.load.side_effect = lambda x: _err()
    return prop


def test_validates(prop, err):
    assert props.AnyOf(err, prop, err).load("thing")


def test_fails(err):
    with pytest.raises(props.PropertyValidationError):
        props.AnyOf(err, err, err).load("thing")


def test_accepts_type(err):
    props.AnyOf(mock.Mock, mock.Mock).load("thing")
