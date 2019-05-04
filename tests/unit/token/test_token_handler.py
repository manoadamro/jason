from unittest import mock

import flask
import pytest

from jason import TokenHandler

config = {
    "key": "123",
    "lifespan": 10,
    "issuer": "test_issuer",
    "audience": "test_audience",
    "algorithm": "HS256",
    "verify": True,
    "auto_update": True,
    "encryption_key": "some-key",
    "require_exp": True,
    "require_nbf": True,
    "require_iat": True,
    "require_aud": True,
    "require_iss": True,
    "verify_exp": True,
    "verify_nbf": True,
    "verify_iat": True,
    "verify_aud": True,
    "verify_iss": True,
    "verify_signature": True,
}


def test_initialisation():
    handler = TokenHandler()
    app = mock.MagicMock(extensions={})
    handler.init_app(app)
    assert "token-handler" in app.extensions


def test_configuration():
    handler = TokenHandler()
    handler.configure(**config)
    assert config["key"] == handler.key
    assert config["lifespan"] == handler.lifespan
    assert config["issuer"] == handler.issuer
    assert config["audience"] == handler.audience
    assert config["algorithm"] == handler.algorithm
    assert config["verify"] == handler.verify
    assert config["auto_update"] == handler.auto_update


def test_use_cipher():
    handler = TokenHandler(encryption_key="secret-key")
    handler.configure(**config)
    assert handler.cipher is not None


def test_use_no_cipher():
    handler = TokenHandler()
    assert handler.cipher is None


def test_invalid_init_kwarg():
    with pytest.raises(ValueError):
        TokenHandler(nope=True)


def test_invalid_configure_kwarg():
    with pytest.raises(ValueError):
        TokenHandler().configure(nope=True)


def test_generate_token_string():
    handler = TokenHandler()
    handler.configure(**config)
    token = handler.generate_token("123", ("read:thing", "write:thing"))
    assert isinstance(token, str)


def test_defaults_algorithm():
    handler = TokenHandler()
    handler.configure(lifespan=10, key="something")
    handler.before_first_request()
    assert handler.algorithm == "HS256"


def test_raises_error_when_missing_lifespan():
    handler = TokenHandler()
    handler.configure(key="something")
    with pytest.raises(ValueError):
        handler.before_first_request()


def test_raises_error_when_missing_key():
    handler = TokenHandler()
    handler.configure(lifespan=10)
    with pytest.raises(ValueError):
        handler.before_first_request()


def test_stores_token_in_g():
    handler = TokenHandler(lifespan=10, key="something", algorithm="HS256")
    token = handler.generate_token()
    with mock.patch("jason.token.handler.flask") as mock_flask:
        mock_flask.g = {}
        mock_flask.request.headers.get.return_value = token
        handler.before_request()
        assert "_ACCESS_TOKEN" in mock_flask.g


def test_skips_missing_token():
    handler = TokenHandler(lifespan=10, key="something", algorithm="HS256")
    with mock.patch("jason.token.handler.flask") as mock_flask:
        mock_flask.g = {}
        mock_flask.request.headers.get.return_value = None
        handler.before_request()
        assert "_ACCESS_TOKEN" not in mock_flask.g


def test_stores_decrypted_token_in_g():
    handler = TokenHandler(
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
    handler = TokenHandler(
        lifespan=10, key="something", algorithm="HS256", auto_update=False
    )
    with mock.patch("jason.token.handler.flask") as mock_flask:
        mock_flask.g = {}
        response = handler.after_request(response)
    assert "Authorization" not in response.headers


def test_auto_update():
    response = flask.Response()
    handler = TokenHandler(
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
