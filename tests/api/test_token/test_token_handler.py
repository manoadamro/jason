from unittest import mock

import pytest

from jason.api.token import TokenHandler, TokenValidationError


@pytest.fixture
def handler():
    return TokenHandler(
        app=mock.MagicMock(),
        key="secret",
        lifespan=10,
        issuer="test-issuer",
        audience="test-audience",
        algorithm="HS256",
        verify=True,
        auto_update=True,
    )


def test_configure_from_init(handler):
    ...


def test_init_app():
    handler = TokenHandler()
    handler.init_app(mock.MagicMock())


def test_configure_explicitly():
    handler = TokenHandler(app=mock.MagicMock())
    handler.configure(
        key="secret",
        lifespan=10,
        issuer="test-issuer",
        audience="test-audience",
        algorithm="HS256",
        verify=True,
        auto_update=True,
    )


def test_configure_decoder_options():
    handler = TokenHandler(app=mock.MagicMock())
    handler.configure(require_exp=True)


def test_configure_unknown_key():
    handler = TokenHandler(app=mock.MagicMock())
    with pytest.raises(ValueError):
        handler.configure(nope=True)


def test_missing_config():
    handler = TokenHandler(app=mock.MagicMock())
    with pytest.raises(ValueError):
        handler.before_first_request()


def test_decode_token_from_header(handler):
    with mock.patch(
        "jason.api.token.flask.request",
        mock.Mock(headers={"Authorization": "Bearer some_token"}),
    ), mock.patch("jason.api.token.flask.g"), mock.patch("jason.api.token.jwt"):
        handler.before_request()


def test_unreadable_token(handler):
    with mock.patch(
        "jason.api.token.flask.request",
        mock.Mock(headers={"Authorization": "some_token"}),
    ), mock.patch("jason.api.token.flask.g"), mock.patch(
        "jason.api.token.jwt"
    ), pytest.raises(
        TokenValidationError
    ):
        handler.before_request()


def test_no_token(handler):
    with mock.patch("jason.api.token.flask.request", mock.Mock(headers={})), mock.patch(
        "jason.api.token.flask.g"
    ), mock.patch("jason.api.token.jwt"):
        handler.before_request()


def test_encode_token_from_header(handler):
    with mock.patch(
        "jason.api.token.flask.request",
        mock.Mock(headers={"Authorization": "Bearer some_token"}),
    ), mock.patch("jason.api.token.flask.g"), mock.patch("jason.api.token.jwt"):
        handler.after_request(mock.MagicMock())


def test_no_auto_update(handler):
    handler.auto_update = False
    handler.after_request(mock.Mock())


def test_generate_token(handler):
    with mock.patch("jason.api.token.jwt"):
        handler.generate_token("123", ["a", "b", "c"])
