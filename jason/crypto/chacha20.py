"""
jason.crypto.chacha20.py

wraps ChaCha20 in Crypto.Cipher from pycryptodome
"""
import base64
import re

from Crypto.Cipher import ChaCha20 as _ChaCha20


class ChaCha20:
    encoding = "utf8"
    _join_char = "-"
    _join_string = _join_char * 2
    _key_length = 32
    _escape = (_join_char, f"%{_join_char}")

    def __init__(self, key):
        key = key.rjust(self._key_length)
        self.key = key.encode(self.encoding)

    def escape(self, string):
        return re.sub(self._escape[0], self._escape[1], string)

    def un_escape(self, string):
        return re.sub(self._escape[1], self._escape[0], string)

    def encrypt(self, plain_text: str) -> str:
        cipher = _ChaCha20.new(key=self.key)
        cipher_bytes = cipher.encrypt(plain_text.encode(self.encoding))
        nonce = base64.b64encode(cipher.nonce).decode(self.encoding)
        cipher_text = base64.b64encode(cipher_bytes).decode(self.encoding)
        return f"{self.escape(cipher_text)}{self._join_string}{self.escape(nonce)}"

    def decrypt(self, encrypted: str) -> str:
        cipher_text, nonce = encrypted.split(self._join_string)
        cipher_text = base64.b64decode(self.un_escape(cipher_text))
        nonce = base64.b64decode(self.un_escape(nonce))
        cipher = _ChaCha20.new(key=self.key, nonce=nonce)
        plain_text = cipher.decrypt(cipher_text)
        return plain_text.decode(self.encoding)
