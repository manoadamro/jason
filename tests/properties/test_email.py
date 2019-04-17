import pytest

from jason import exceptions
from jason.properties import Email


VALID_EMAILS = [
    # TODO write a regex matcher to validate these... good luck
    # "email@domain.com",
    # "firstname.lastname@domain.com",
    # "email@subdomain.domain.com",
    # "firstname+lastname@domain.com",
    # "email@123.123.123.123",
    # "email@[123.123.123.123]",
    # '"email"@domain.com',
    # "1234567890@domain.com",
    # "email@domain-one.com",
    # "_______@domain.com",
    # "email@domain.name",
    # "email@domain.co.jp",
    # "firstname-lastname@domain.com"
]

INVALID_EMAILS = [
    # TODO write a regex matcher to invalidate these... good luck
    # "plainaddress",
    # "#@%^%#$@#$@#.com",
    # "@domain.com",
    # "Joe Smith <email@domain.com>",
    # "email.domain.com",
    # "email@domain@domain.com",
    # ".email@domain.com",
    # "email.@domain.com",
    # "email..email@domain.com",
    # "あいうえお@domain.com",
    # "email@domain.com (Joe Smith)",
    # "email@domain",
    # "email@-domain.com",
    # "email@111.222.333.44444",
    # "email@domain..com"
]


def test_positive():
    for email in VALID_EMAILS:
        prop = Email()
        try:
            assert prop.load(email) == email, f"could not validate: {email}"
        except exceptions.PropertyValidationError:
            raise AssertionError(f"could not validate: {email}")


def test_negative():
    for email in INVALID_EMAILS:
        prop = Email()
        with pytest.raises(exceptions.PropertyValidationError):
            prop.load(email)
            pytest.fail(f"wrongly validated: {email}")
