import pytest

from jason.properties import Uuid


def test_valid_uuid_with_hyphens():
    uuid = "672626ce-3cab-46db-8e7a-67cb1e5e75c2"
    prop = Uuid()
    assert prop.load(uuid) == uuid


def test_valid_uuid_without_hyphens():
    uuid = "672626ce3cab46db8e7a67cb1e5e75c2"
    prop = Uuid()
    assert prop.load(uuid) == uuid


def test_invalid_uuid():
    uuid = "not-a-uuid"
    prop = Uuid()
    with pytest.raises(Exception):
        prop.load(uuid)
