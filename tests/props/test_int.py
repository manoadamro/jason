import pytest

from jason.props import Int, PropertyValidationError


def test_does_not_accept_float():
    prop = Int()
    with pytest.raises(PropertyValidationError):
        prop.load(12.5)