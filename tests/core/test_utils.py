import unittest.mock as mock

from jason import utils


def test_maybe_call_with_callable():
    mock_callable = mock.Mock(return_value=123)
    assert utils.maybe_call(mock_callable) == 123


def test_maybe_call_with_value():
    assert utils.maybe_call(123) == 123


def test_is_type_with_specific_type():
    assert utils.is_type(int, typ=int) is True


def test_is_type_with_any_type():
    assert utils.is_type(int) is True


def test_is_type_with_instance():
    assert utils.is_type(123) is False


def test_is_instance_or_type_with_type():
    assert utils.is_instance_or_type(int, typ=int) is True


def test_is_instance_or_type_with_wrong_type():
    assert utils.is_instance_or_type(int, typ=int) is True


def test_is_instance_or_type_with_instance():
    assert utils.is_instance_or_type(bool, typ=str) is False


def test_is_instance_or_type_with_wrong_instance():
    assert utils.is_instance_or_type(123, typ=bool) is False
