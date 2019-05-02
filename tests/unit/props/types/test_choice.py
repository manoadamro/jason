import pytest

from jason import props


def test_validates():
    assert props.Choice(choices=[1, 2, 3]).load(2)


def test_fails():
    with pytest.raises(props.PropertyValidationError):
        assert props.Choice(choices=[1, 2, 3]).load(5)


def test_nullable():
    props.Choice(choices=[1, 2, 3], nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Choice(choices=[1, 2, 3]).load(None)


def test_default():
    assert props.Choice(choices=[1, 2, 3], default=2).load(None) == 2
