import flask
import pytest

from jason import jsonify
from jason.service import JSONEncoder


def test_patches_original():
    assert flask.jsonify is jsonify


def test_single():
    with flask.Flask(__name__).app_context():
        assert flask.jsonify({"uuid": "1", "x": True}).json == {"uuid": "1", "x": True}


def test_single_fails_with_key():
    with flask.Flask(__name__).app_context(), pytest.raises(ValueError):
        assert flask.jsonify({"uuid": "1", "x": True}, key="uuid").json == {
            "uuid": "1",
            "x": True,
        }


def test_iterable():
    with flask.Flask(__name__).app_context():
        assert flask.jsonify(
            [
                {"uuid": "1", "x": True},
                {"uuid": "2", "x": False},
                {"uuid": "3", "x": True},
            ]
        ).json == [
            {"uuid": "1", "x": True},
            {"uuid": "2", "x": False},
            {"uuid": "3", "x": True},
        ]


def test_iterable_with_key():
    with flask.Flask(__name__).app_context():
        assert flask.jsonify(
            [
                {"uuid": "1", "x": True},
                {"uuid": "2", "x": False},
                {"uuid": "3", "x": True},
            ],
            key="uuid",
        ).json == {
            "1": {"uuid": "1", "x": True},
            "2": {"uuid": "2", "x": False},
            "3": {"uuid": "3", "x": True},
        }


def test_iterable_object():
    @JSONEncoder.encode_all
    class Thing:
        def __init__(self, uuid, x):
            self.uuid = uuid
            self.x = x

    app = flask.Flask(__name__)
    app.json_encoder = JSONEncoder
    with app.app_context():
        assert flask.jsonify(
            [Thing("1", True), Thing("2", False), Thing("3", True)], key="uuid"
        ).json == {
            "1": {"uuid": "1", "x": True},
            "2": {"uuid": "2", "x": False},
            "3": {"uuid": "3", "x": True},
        }
