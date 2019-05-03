import pytest

from jason import props


def test_nullable():
    props.Password(nullable=True).load(None)


def test_not_nullable():
    with pytest.raises(props.PropertyValidationError):
        props.Password().load(None)


def test_wrong_type():
    with pytest.raises(props.PropertyValidationError):
        props.Password().load(12345)


def test_default():
    assert props.Password(default="12345").load(None) == "12345"


def test_too_short():
    with pytest.raises(props.PropertyValidationError):
        props.Password(min_length=10).load("123")


def test_too_long():
    with pytest.raises(props.PropertyValidationError):
        props.Password(max_length=2).load("123")


def test_enforce_no_whitespace_passes():
    with pytest.raises(props.PropertyValidationError):
        props.Password().load("1 2 3")


def test_enforce_uppercase_fails():
    with pytest.raises(props.PropertyValidationError):
        props.Password(uppercase=True).load("abc")


def test_enforce_uppercase():
    assert props.Password(uppercase=True).load("ABC") == "ABC"


def test_enforce_no_uppercase_fails():
    with pytest.raises(props.PropertyValidationError):
        props.Password(uppercase=False).load("ABC")


def test_enforce_no_uppercase():
    assert props.Password(uppercase=False).load("abc") == "abc"


def test_enforce_numbers_fails():
    with pytest.raises(props.PropertyValidationError):
        props.Password(numbers=True).load("abc")


def test_enforce_numbers():
    assert props.Password(numbers=True).load("123") == "123"


def test_enforce_no_numbers_fails():
    with pytest.raises(props.PropertyValidationError):
        props.Password(numbers=False).load("123")


def test_enforce_no_numbers():
    assert props.Password(numbers=False).load("abc") == "abc"


def test_enforce_symbols_fails():
    with pytest.raises(props.PropertyValidationError):
        props.Password(symbols=True).load("abc")


def test_enforce_symbols():
    assert props.Password(symbols=True).load("ab$") == "ab$"


def test_enforce_no_symbols_fails():
    with pytest.raises(props.PropertyValidationError):
        props.Password(symbols=False).load("ab$")


def test_enforce_no_symbols():
    assert props.Password(symbols=False).load("abc") == "abc"


def test_score():
    with pytest.raises(props.PropertyValidationError):
        assert props.Password(score=3).load("abc")
    with pytest.raises(props.PropertyValidationError):
        assert props.Password(score=3).load("aBc")
    with pytest.raises(props.PropertyValidationError):
        assert props.Password(score=3).load("1Bc")
    assert props.Password(score=3).load("1Bc$") == "1Bc$"
