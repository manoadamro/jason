from unittest import mock

import flask
import pytest

from jason import Handler

config = {
    "key": "123",
    "lifespan": 10,
    "issuer": "test_issuer",
    "audience": "test_audience",
    "algorithm": "HS256",
    "verify": True,
    "auto_update": True,
    "encryption_key": "some-key",
}


def test_initialisation():
    handler = Handler()
    app = mock.MagicMock(extensions={})
    handler.init_app(app)
    assert "token-handler" in app.extensions


def test_configuration():
    handler = Handler()
    handler.configure(**config)
    assert config["key"] == handler.key
    assert config["lifespan"] == handler.lifespan
    assert config["issuer"] == handler.issuer
    assert config["audience"] == handler.audience
    assert config["algorithm"] == handler.algorithm
    assert config["verify"] == handler.verify
    assert config["auto_update"] == handler.auto_update


def test_use_cipher():
    handler = Handler(encryption_key="secret-key")
    handler.configure(**config)
    assert handler.cipher is not None


def test_use_no_cipher():
    handler = Handler()
    assert handler.cipher is None


def test_invalid_init_kwarg():
    with pytest.raises(ValueError):
        Handler(nope=True)


def test_invalid_configure_kwarg():
    with pytest.raises(ValueError):
        Handler().configure(nope=True)


def test_generate_token_string():
    handler = Handler()
    handler.configure(**config)
    token = handler.generate_token("123", ("read:thing", "write:thing"))
    assert isinstance(token, str)


def test_defaults_algorithm():
    handler = Handler()
    handler.configure(lifespan=10, key="something")
    handler.before_first_request()
    assert handler.algorithm == "HS256"


def test_raises_error_when_missing_lifespan():
    handler = Handler()
    handler.configure(key="something")
    with pytest.raises(ValueError):
        handler.before_first_request()


def test_raises_error_when_missing_key():
    handler = Handler()
    handler.configure(lifespan=10)
    with pytest.raises(ValueError):
        handler.before_first_request()


def test_stores_token_in_g():
    handler = Handler(lifespan=10, key="something", algorithm="HS256")
    token = handler.generate_token()
    with mock.patch("jason.token.handler.flask") as mock_flask:
        mock_flask.g = {}
        mock_flask.request.headers.get.return_value = token
        handler.before_request()
        assert "_ACCESS_TOKEN" in mock_flask.g


def test_skips_missing_token():
    handler = Handler(lifespan=10, key="something", algorithm="HS256")
    with mock.patch("jason.token.handler.flask") as mock_flask:
        mock_flask.g = {}
        mock_flask.request.headers.get.return_value = None
        handler.before_request()
        assert "_ACCESS_TOKEN" not in mock_flask.g


def test_stores_decrypted_token_in_g():
    handler = Handler(
        lifespan=10, key="something", algorithm="HS256", encryption_key="something"
    )
    token = handler.generate_token()
    with mock.patch("jason.token.handler.flask") as mock_flask:
        mock_flask.g = {}
        mock_flask.request.headers.get.return_value = token
        handler.before_request()
        assert "_ACCESS_TOKEN" in mock_flask.g


def test_skips_if_not_auto_update():
    response = flask.Response()
    handler = Handler(
        lifespan=10, key="something", algorithm="HS256", auto_update=False
    )
    with mock.patch("jason.token.handler.flask") as mock_flask:
        mock_flask.g = {}
        response = handler.after_request(response)
    assert "Authorization" not in response.headers


def test_auto_update():
    response = flask.Response()
    handler = Handler(
        lifespan=10,
        key="something",
        algorithm="HS256",
        auto_update=True,
        encryption_key="something",
    )
    with mock.patch("jason.token.handler.flask") as mock_flask:
        mock_flask.g = {"_ACCESS_TOKEN": {}}
        response = handler.after_request(response)
    assert "Authorization" in response.headers
