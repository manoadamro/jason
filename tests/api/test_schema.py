import uuid

import flask
import pytest
from jason.api.schema import props, request_schema


@pytest.fixture
def query():
    return props.Inline(props=dict(q=props.String, i=props.Int(nullable=True)))


@pytest.fixture
def params():
    return props.Inline(props=dict(uuid=props.Uuid))


@pytest.fixture
def json():
    return props.Inline(props=dict(thing=props.Bool))


@pytest.fixture
def app():
    return flask.Flask(__name__)


@pytest.fixture
def inline_schema(query, params, json):
    return request_schema(query=query, params=params, json=json)


@pytest.fixture
def model_schema(query, params, json):
    q = query
    p = params
    j = json

    class RequestModel:
        query = q
        Params = p
        JSON = j

    return request_schema(model=RequestModel)


def test_request_schema(inline_schema, app):
    @inline_schema
    def request_func(uuid, query, json, form):
        return uuid, query, json, form

    uid = str(uuid.uuid4())
    with app.test_request_context(path=f"/thing/{uid}?q=thingy", json={"thing": True}):
        flask.request.view_args = dict(uuid=uid)
        response = request_func()

    assert response[0] == uid
    assert response[1] == {"q": "thingy", "i": None}
    assert response[2] == {"thing": True}
    assert response[3] == {}


def test_schema_from_model(model_schema, app):
    @model_schema
    def request_func(uuid, query, json, form):
        return uuid, query, json, form

    uid = str(uuid.uuid4())
    with app.test_request_context(path=f"/thing/{uid}?q=thingy", json={"thing": True}):
        flask.request.view_args = dict(uuid=uid)
        response = request_func()

    assert response[0] == uid
    assert response[1] == {"q": "thingy", "i": None}
    assert response[2] == {"thing": True}
    assert response[3] == {}
