from unittest import mock

import pytest

from jason.token import TokenHandler, TokenValidationError


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
        encryption_key="secret",
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
        encryption_key="secret",
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
    token = handler.cipher.encrypt("some_token")
    with mock.patch(
        "jason.token.flask.request", mock.Mock(headers={"Authorization": token})
    ), mock.patch("jason.token.flask.g"), mock.patch("jason.token.jwt"):
        handler.before_request()


def test_no_token(handler):
    with mock.patch("jason.token.flask.request", mock.Mock(headers={})), mock.patch(
        "jason.token.flask.g"
    ), mock.patch("jason.token.jwt"):
        handler.before_request()


def test_encode_token(handler):
    with mock.patch("jason.token.flask.g", mock.MagicMock()), mock.patch(
        "jason.token.jwt", mock.Mock(encode=mock.Mock(return_value="something"))
    ):
        handler.after_request(mock.MagicMock())


def test_no_auto_update(handler):
    handler.auto_update = False
    handler.after_request(mock.Mock())


def test_generate_token(handler):
    with mock.patch("jason.token.jwt") as mock_jwt:
        mock_jwt.encode.side_effect = lambda payload, **kwargs: str(payload)
        handler.generate_token("123", ["a", "b", "c"])
