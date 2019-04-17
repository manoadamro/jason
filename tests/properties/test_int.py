import pytest

from jason import exceptions
from jason.properties import Int


def test_does_not_accept_float():
    prop = Int()
    with pytest.raises(exceptions.PropertyValidationError):
        prop.load(12.5)
