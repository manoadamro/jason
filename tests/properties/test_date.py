import datetime

import pytest

from jason.properties import Date, PropertyValidationError


@pytest.fixture
def minimum():
    return datetime.date(year=2000, month=1, day=1)


@pytest.fixture
def maximum():
    return datetime.date(year=2001, month=1, day=1)


def test_value_too_low(minimum, maximum):
    prop = Date(min_value=minimum, max_value=maximum)
    with pytest.raises(PropertyValidationError):
        prop.load(datetime.date(year=1999, month=1, day=1))


def test_value_too_high(minimum, maximum):
    prop = Date(min_value=minimum, max_value=maximum)
    with pytest.raises(PropertyValidationError):
        prop.load(datetime.date(year=2002, month=1, day=1))


def test_no_min(maximum):
    dt = datetime.date(year=1999, month=1, day=1)
    prop = Date(min_value=None, max_value=maximum)
    assert prop.load(dt) == dt


def test_no_max(minimum):
    dt = datetime.date(year=2002, month=1, day=1)
    prop = Date(min_value=minimum, max_value=None)
    assert prop.load(dt) == dt


def test_no_range():
    dt = datetime.date(year=2002, month=1, day=1)
    prop = Date(min_value=None, max_value=None)
    assert prop.load(dt) == dt


def test_date_from_string():
    prop = Date(allow_strings=True)
    assert prop.load("2000-01-01") == datetime.date(year=2000, month=1, day=1)


def test_string_date_when_strings_not_allowed():
    prop = Date(allow_strings=False)
    with pytest.raises(PropertyValidationError):
        prop.load("2000-01-01")


def test_invalid_date_from_string():
    prop = Date(allow_strings=True)
    with pytest.raises(PropertyValidationError):
        prop.load("2001-02-29")


def test_nan_from_string():
    prop = Date(allow_strings=True)
    with pytest.raises(PropertyValidationError):
        prop.load("nope")
