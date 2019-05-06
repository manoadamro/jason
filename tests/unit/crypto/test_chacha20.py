import pytest

from jason.crypto import ChaCha20


@pytest.fixture
def cipher():
    return ChaCha20("secret-key")


def test_escape(cipher):
    assert cipher.escape("some-thing-secret") == "some%-thing%-secret"


def test_unescape(cipher):
    assert cipher.un_escape("some%-thing%-secret") == "some-thing-secret"


def test_encrypt(cipher):
    string = "some-secret-message"
    encrypted = cipher.encrypt(string)
    assert encrypted != string


def test_encrypts_to_string(cipher):
    string = "some-secret-message"
    encrypted = cipher.encrypt(string)
    assert isinstance(encrypted, str)


def test_decrypts(cipher):
    string = "some-secret-message"
    encrypted = cipher.encrypt(string)
    assert cipher.decrypt(encrypted) == string


def test_decrypts_to_string(cipher):
    string = "some-secret-message"
    encrypted = cipher.encrypt(string)
    decrypted = cipher.decrypt(encrypted)
    assert isinstance(decrypted, str)
