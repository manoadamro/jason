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
    assert props.Array(prop).load([1, 2, 3, 4])


def test_fails(err):
    with pytest.raises(props.BatchValidationError):
        props.Array(err).load([1, 2, 3, 4])


def test_accepts_type(err):
    props.Array(mock.Mock).load([1, 2, 3, 4])


def test_too_short():
    with pytest.raises(props.PropertyValidationError):
        props.Array(mock.Mock, min_length=10).load([1, 2, 3, 4])


def test_too_long():
    with pytest.raises(props.PropertyValidationError):
        props.Array(mock.Mock, max_length=2).load([1, 2, 3, 4])


def test_nullable():
    props.Array(mock.Mock, nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Array(mock.Mock).load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Array(mock.Mock).load("12345")


def test_default():
    mock_prop = mock.Mock()
    mock_prop.load.side_effect = lambda x: x
    assert props.Array(mock_prop, default=[1, 2, 3, 4]).load(None) == [1, 2, 3, 4]
