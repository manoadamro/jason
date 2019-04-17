import pytest

from jason import exceptions
from jason.properties import Password


def test_fails_when_contains_whitespace():
    prop = Password()
    with pytest.raises(exceptions.PropertyValidationError):
        prop.load("my pa$$w0rd")


def test_fails_uppercase():
    prop = Password(uppercase=True)
    with pytest.raises(exceptions.PropertyValidationError):
        prop.load("pa$$w0rd")


def test_illegal_uppercase():
    prop = Password(uppercase=False)
    with pytest.raises(exceptions.PropertyValidationError):
        prop.load("Pa$$w0rd")


def test_passes_uppercase():
    prop = Password(uppercase=True)
    assert prop.load("Pa$$w0rd") == "Pa$$w0rd"


def test_fails_numbers():
    prop = Password(numbers=True)
    with pytest.raises(exceptions.PropertyValidationError):
        prop.load("Pa$$word")


def test_illegal_numbers():
    prop = Password(numbers=False)
    with pytest.raises(exceptions.PropertyValidationError):
        prop.load("Pa$$w0rd")


def test_passes_numbers():
    prop = Password(numbers=True)
    assert prop.load("Pa$$w0rd") == "Pa$$w0rd"


def test_fails_symbols():
    prop = Password(symbols=True)
    with pytest.raises(exceptions.PropertyValidationError):
        prop.load("Passw0rd")


def test_illegal_symbols():
    prop = Password(symbols=False)
    with pytest.raises(exceptions.PropertyValidationError):
        prop.load("Pa$$w0rd")


def test_passes_symbols():
    prop = Password(symbols=True)
    assert prop.load("Pa$$w0rd") == "Pa$$w0rd"
