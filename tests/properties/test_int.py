import pytest

from jason.properties import Int


def test_does_not_accept_float():
    prop = Int()
    with pytest.raises(Exception):
        prop.load(12.5)
