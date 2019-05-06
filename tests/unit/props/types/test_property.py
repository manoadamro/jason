import pytest

from jason import props


def test_nullable():
    props.Property(nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Property().load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Property(types=(int,)).load("12345")


def test_default():
    assert props.Property(default=True).load(None) is True


def test_decorator():
    @props.Int()
    def my_int(value):
        return value * 2

    assert my_int.load(123) == 246
