import re
from typing import Pattern

import pytest

from jason.core.schema import PropertyValidationError, Regex


@pytest.fixture
def matcher():
    return re.compile("^[a-zA-Z]{4}$")


def test_auto_compiles():
    prop = Regex("[a-zA-Z]{3}")
    assert isinstance(prop.matcher, Pattern)


def test_matches_string(matcher):
    prop = Regex(matcher=matcher)
    assert prop.load("aBcD") == "aBcD"


def test_fails_to_match_string(matcher):
    prop = Regex(matcher=matcher)
    with pytest.raises(PropertyValidationError):
        assert prop.load("aB3D")
