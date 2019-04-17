import pytest

from jason.properties import Number


def test_value_too_low():
    prop = Number(min_value=10, max_value=20)
    with pytest.raises(Exception):
        prop.load(5)


def test_value_too_high():
    prop = Number(min_value=10, max_value=20)
    with pytest.raises(Exception):
        prop.load(25)


def test_no_min():
    prop = Number(min_value=None, max_value=20)
    assert prop.load(5) == 5


def test_no_max():
    prop = Number(min_value=10, max_value=None)
    assert prop.load(25) == 25


def test_no_range():
    prop = Number(min_value=None, max_value=None)
    assert prop.load(5) == 5
