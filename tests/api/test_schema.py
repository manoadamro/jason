from contextlib import contextmanager
from unittest import mock

import pytest
from jason.api import schema


def mock_request(args=None, query=None, json=None, form=None):
    return mock.Mock(
        view_args=args, args=query, json=json, form=form, is_json=json is not None
    )


@contextmanager
def patch_request(**kwargs):
    with mock.patch("jason.api.schema.request", mock_request(**kwargs)) as request:
        try:
            yield request
        finally:
            ...


def test_validates_request_query():
    @schema.request_schema(
        query=schema.props.Inline(
            props=dict(q=schema.props.String, i=schema.props.Int(nullable=True))
        )
    )
    def mock_route(query):
        return query

    with patch_request(query=dict(q="hello")):
        parsed_query = mock_route()

    assert parsed_query == {"i": None, "q": "hello"}


def test_validates_request_view_args():
    @schema.request_schema(
        args=schema.props.Inline(
            props=dict(thing_id=schema.props.Int, other_id=schema.props.Int)
        )
    )
    def mock_route(thing_id, other_id):
        return thing_id, other_id

    with patch_request(args=dict(thing_id=123, other_id=456)):
        parsed_args = mock_route()

    assert parsed_args == (123, 456)


def test_validates_request_json():
    @schema.request_schema(
        json=schema.props.Inline(
            props=dict(q=schema.props.String, i=schema.props.Int(nullable=True))
        )
    )
    def mock_route(json):
        return json

    with patch_request(json=dict(q="hello")):
        parsed_json = mock_route()

    assert parsed_json == {"i": None, "q": "hello"}


def test_json_true():
    @schema.request_schema(json=True)
    def mock_route(json):
        return json

    with patch_request(json=dict(q="hello")):
        parsed_json = mock_route()

    assert parsed_json == {"q": "hello"}

    with patch_request(json=None), pytest.raises(schema.RequestValidationError):
        mock_route()


def test_json_false():
    @schema.request_schema(json=False)
    def mock_route(json):
        return json

    with patch_request(json=None):
        parsed_json = mock_route()

    assert parsed_json is None

    with patch_request(json=dict(q="hello")), pytest.raises(
        schema.RequestValidationError
    ):
        mock_route()


def test_json_none():
    @schema.request_schema(json=None)
    def mock_route(json):
        return json

    with patch_request(json=dict(q="hello")):
        parsed_json = mock_route()

    assert parsed_json == {"q": "hello"}

    with patch_request(json=None):
        parsed_json = mock_route()

    assert parsed_json is None


def test_validates_request_form():
    @schema.request_schema(
        form=schema.props.Inline(
            props=dict(q=schema.props.String, i=schema.props.Int(nullable=True))
        )
    )
    def mock_route(form):
        return form

    with patch_request(form=dict(q="hello")):
        parsed_form = mock_route()

    assert parsed_form == {"i": None, "q": "hello"}


def test_form_true():
    @schema.request_schema(form=True)
    def mock_route(form):
        return form

    with patch_request(form=dict(q="hello")):
        parsed_form = mock_route()

    assert parsed_form == {"q": "hello"}

    with patch_request(form=None), pytest.raises(schema.RequestValidationError):
        mock_route()


def test_form_false():
    @schema.request_schema(form=False)
    def mock_route(form):
        return form

    with patch_request(form=None):
        parsed_form = mock_route()

    assert parsed_form is None

    with patch_request(form=dict(q="hello")), pytest.raises(
        schema.RequestValidationError
    ):
        mock_route()


def test_form_none():
    @schema.request_schema(form=None)
    def mock_route(form):
        return form

    with patch_request(form=dict(q="hello")):
        parsed_form = mock_route()

    assert parsed_form == {"q": "hello"}

    with patch_request(json=None):
        parsed_form = mock_route()

    assert parsed_form is None


@pytest.fixture
def model():
    class MyModel:

        args = schema.props.Inline(
            props=dict(thing_id=schema.props.Int, other_id=schema.props.Int)
        )

        JSON = schema.props.Inline(props=dict(name=schema.props.String))

        class Query:
            i = schema.props.Int

    return MyModel


def test_validates_request_from_model(model):
    @schema.request_schema(model=model)
    def mock_route(thing_id, other_id, json, query):
        return thing_id, other_id, json, query

    with patch_request(
        query=dict(q=789),
        json=dict(name="hello"),
        args=dict(thing_id=123, other_id=456),
    ):
        thing_id, other_id, parsed_json, parsed_query = mock_route()

    assert thing_id == 123
    assert other_id == 456
    assert parsed_json == {"name": "hello"}
    assert parsed_query == {"q": 789}


def test_kwargs_override_model(model):
    @schema.request_schema(
        model=model, json=schema.props.Inline(props=dict(age=schema.props.Int))
    )
    def mock_route(thing_id, other_id, json):
        return thing_id, other_id, json

    with patch_request(json=dict(age=30), args=dict(thing_id=123, other_id=456)):
        thing_id, other_id, parsed_json = mock_route()

    assert thing_id == 123
    assert other_id == 456
    assert parsed_json == {"age": 30}
