import pytest

from jason.props import PropertyValidationError
from jason.props.range import DateTimeRangeCheck


@pytest.fixture
def range():
    return DateTimeRangeCheck("1970-01-01T00:00:00.000Z", "2000-01-01T00:00:00.000Z")


def test_validates_correct_value(range):
    range.validate("1990-01-01T00:00:00.000Z")


def test_implicit_utc(range):
    range.validate("1990-01-01T00:00:00.000")


def test_date(range):
    DateTimeRangeCheck("1970-01-01", "2000-01-01").validate("1990-01-01")


def test_raises_error_when_too_low(range):
    with pytest.raises(PropertyValidationError):
        range.validate("1945-01-01T00:00:00.000Z")


def test_raises_error_when_too_high(range):
    with pytest.raises(PropertyValidationError):
        range.validate("2010-01-01T00:00:00.000Z")
