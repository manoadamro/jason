import pytest

from jason.props import PropertyValidationError
from jason.props.range import SizeRangeCheck


@pytest.fixture
def range():
    return SizeRangeCheck(3, 5)


def test_validates_correct_value(range):
    range.validate([1, 2, 3, 4])


def test_raises_error_when_too_low(range):
    with pytest.raises(PropertyValidationError):
        range.validate([1, 2])


def test_raises_error_when_too_high(range):
    with pytest.raises(PropertyValidationError):
        range.validate([1, 2, 3, 4, 5, 6, 7])
