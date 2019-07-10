import datetime
import uuid
from unittest import mock

import pytest

from jason.service.encoder import JSONEncoder


def test_static_registry_from_instance():
    JSONEncoder().object(int)(lambda i: i * 2)
    assert int in JSONEncoder._object_encoders.keys()


def test_static_registry_from_type():
    JSONEncoder.object(int)(lambda i: i * 2)
    assert int in JSONEncoder._object_encoders.keys()


def test_registered_encoder_is_called():
    class Thing:
        ...

    mock_encoder = mock.Mock(return_value="thing")
    JSONEncoder.object(Thing)(mock_encoder)
    encoded = JSONEncoder().encode({"x": Thing()})
    assert mock_encoder.call_count == 1
    assert encoded == '{"x": "thing"}'


def test_uses_default_for_unregistered():
    mock_encoder = mock.Mock(return_value="nope")
    encoded = JSONEncoder().encode(
        {"x": uuid.UUID("6faf7e15-ef23-482d-935b-62a37abc0df4")}
    )
    assert mock_encoder.call_count == 0
    assert encoded == '{"x": "6faf7e15-ef23-482d-935b-62a37abc0df4"}'


def test_handles_datetime():
    mock_encoder = mock.Mock(return_value="nope")
    encoded = JSONEncoder().encode(
        {"x": datetime.datetime(year=1970, month=1, day=1, hour=1, minute=1, second=1)}
    )
    assert mock_encoder.call_count == 0
    assert encoded == '{"x": "1970-01-01T01:01:01"}'


def test_handles_date():
    mock_encoder = mock.Mock(return_value="nope")
    encoded = JSONEncoder().encode({"x": datetime.date(year=1970, month=1, day=1)})
    assert mock_encoder.call_count == 0
    assert encoded == '{"x": "1970-01-01"}'