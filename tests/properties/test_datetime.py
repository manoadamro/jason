import datetime

import pytest

from jason import exceptions
from jason.properties import Datetime


@pytest.fixture
def minimum():
    return datetime.datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1)


@pytest.fixture
def maximum():
    return datetime.datetime(year=2001, month=1, day=1, hour=1, minute=1, second=1)


def test_value_too_low(minimum, maximum):
    prop = Datetime(min_value=minimum, max_value=maximum)
    with pytest.raises(exceptions.PropertyValidationError):
        prop.load(
            datetime.datetime(year=1999, month=1, day=1, hour=1, minute=1, second=1)
        )


def test_value_too_high(minimum, maximum):
    prop = Datetime(min_value=minimum, max_value=maximum)
    with pytest.raises(exceptions.PropertyValidationError):
        prop.load(
            datetime.datetime(year=2002, month=1, day=1, hour=1, minute=1, second=1)
        )


def test_no_min(maximum):
    dt = datetime.datetime(year=1999, month=1, day=1, hour=1, minute=1, second=1)
    prop = Datetime(min_value=None, max_value=maximum)
    assert prop.load(dt) == dt


def test_no_max(minimum):
    dt = datetime.datetime(year=2002, month=1, day=1, hour=1, minute=1, second=1)
    prop = Datetime(min_value=minimum, max_value=None)
    assert prop.load(dt) == dt


def test_no_range():
    dt = datetime.datetime(year=2002, month=1, day=1, hour=1, minute=1, second=1)
    prop = Datetime(min_value=None, max_value=None)
    assert prop.load(dt) == dt


def test_date_from_string():
    prop = Datetime(allow_strings=True)
    assert prop.load("2000-01-01T01:01:01.000+01:00") == datetime.datetime(
        year=2000,
        month=1,
        day=1,
        hour=1,
        minute=1,
        second=1,
        tzinfo=datetime.timezone(datetime.timedelta(hours=1)),
    )


def test_string_date_when_strings_not_allowed():
    prop = Datetime(allow_strings=False)
    with pytest.raises(exceptions.PropertyValidationError):
        prop.load("2000-01-01T01:01:01.000+00:00")


def test_invalid_date_from_string():
    prop = Datetime(allow_strings=True)
    with pytest.raises(exceptions.PropertyValidationError):
        prop.load("2001-02-29T01:01:01.000+00:00")


def test_nan_from_string():
    prop = Datetime(allow_strings=True)
    with pytest.raises(exceptions.PropertyValidationError):
        prop.load("nope")


def test_handles_z():
    prop = Datetime(allow_strings=True)
    assert prop.load("2000-01-01T01:01:01.000Z") == datetime.datetime(
        year=2000,
        month=1,
        day=1,
        hour=1,
        minute=1,
        second=1,
        tzinfo=datetime.timezone(datetime.timedelta(hours=0)),
    )
