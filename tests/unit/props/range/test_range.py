import pytest

from jason.props import PropertyValidationError
from jason.props.range import RangeCheck


@pytest.fixture
def range():
    return RangeCheck(5, 10)


def test_validates_correct_value(range):
    range.validate(7)


def test_raises_error_when_too_low(range):
    with pytest.raises(PropertyValidationError):
        range.validate(2)


def test_raises_error_when_too_high(range):
    with pytest.raises(PropertyValidationError):
        range.validate(15)
