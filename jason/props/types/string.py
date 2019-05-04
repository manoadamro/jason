import re
import uuid
from typing import Any, Callable, Pattern, Union

from .. import error, range
from .property import Property


class String(Property):
    def __init__(
        self,
        min_length: Union[Callable[[], int], int] = None,
        max_length: Union[Callable[[], int], int] = None,
        **kwargs: Any,
    ):
        super(String, self).__init__(types=(str,), **kwargs)
        self.range = range.SizeRangeCheck(min_value=min_length, max_value=max_length)

    def _validate(self, value: str) -> str:
        self.range.validate(value)
        return value


class Regex(String):
    def __init__(self, matcher: Union[str, Pattern], **kwargs: Any):
        super(Regex, self).__init__(**kwargs)
        if isinstance(matcher, str):
            matcher = re.compile(matcher)
        self.matcher = matcher

    def _validate(self, value: str) -> str:
        value = super(Regex, self)._validate(value)
        if re.match(self.matcher, value) is None:
            raise error.PropertyValidationError(
                f"String value '{value}' did not match regex pattern '{self.matcher.pattern}'"
            )
        return value


class Uuid(String):
    def __init__(self, **kwargs):
        super(Uuid, self).__init__(**kwargs)

    def _validate(self, value: str) -> str:
        value = super(Uuid, self)._validate(value)
        try:
            uuid.UUID(value)
        except ValueError:
            raise error.PropertyValidationError(f"value '{value}' is not a valid uuid")
        return value


class Password(String):

    uppercase_matcher = re.compile("[A-Z]")
    numbers_matcher = re.compile("[0-9]")
    symbols_matcher = re.compile("[^A-Za-z0-9]")
    whitespace_matcher = re.compile("[\\s]")
    max_score = 3

    def __init__(
        self,
        uppercase: bool = None,
        numbers: bool = None,
        symbols: bool = None,
        score: int = 0,
        **kwargs: Any,
    ):
        super(Password, self).__init__(**kwargs)
        self.uppercase = uppercase
        self.numbers = numbers
        self.symbols = symbols
        self.min_score = min(score, self.max_score)

    def _validate(self, value: str) -> str:
        value = super(Password, self)._validate(value)
        score = 0
        if re.search(self.whitespace_matcher, value):
            raise error.PropertyValidationError(
                f"Password must not contain white space"
            )

        if re.search(self.uppercase_matcher, value):
            if self.uppercase is False:
                raise error.PropertyValidationError(
                    f"Password must not contain uppercase characters"
                )
            score += 1
        elif self.uppercase is True:
            raise error.PropertyValidationError(
                f"Password must contain at least 1 uppercase character"
            )

        if re.search(self.numbers_matcher, value):
            if self.numbers is False:
                raise error.PropertyValidationError(
                    f"Password must not contain numbers"
                )
            score += 1
        elif self.numbers is True:
            raise error.PropertyValidationError(
                f"Password must contain at least 1 number"
            )

        if re.search(self.symbols_matcher, value):
            if self.symbols is False:
                raise error.PropertyValidationError(
                    f"Password must not contain symbol characters"
                )
            score += 1
        elif self.symbols is True:
            raise error.PropertyValidationError(
                f"Password must contain at least 1 symbol character"
            )

        if score < self.min_score:
            raise error.PropertyValidationError(
                f"Password is too weak. "
                f"minimum score: {self.min_score}. "
                f"current score: {score}"
            )

        return value


class Email(Regex):
    matcher = re.compile("^[^@]+@[^@]+\\.[^@]+$")

    def __init__(self, **kwargs: Any):
        super(Email, self).__init__(self.matcher, **kwargs)
