from Crypto.Cipher import AES as _AES
from Crypto.Util.Padding import pad as _pad

import base64
import re


class AES:
    encoding = "utf8"
    _join_char = "-"
    _join_string = _join_char * 2
    _key_length = 32
    _escape = (_join_char, f"%{_join_char}")
    _mode = _AES.MODE_CTR

    def __init__(self, key: str):
        key = key.rjust(self._key_length)
        self.key = bytearray(key.encode(self.encoding))
        self.key = bytes([self.key[c % len(self.key)] for c in range(0, 16)])

    def escape(self, string: str) -> str:
        return re.sub(self._escape[0], self._escape[1], string)

    def un_escape(self, string: str) -> str:
        return re.sub(self._escape[1], self._escape[0], string)

    def encrypt(self, plain_text: str) -> str:
        cipher = _AES.new(key=self.key, mode=self._mode)
        if isinstance(plain_text, str):
            plain_text = plain_text.encode(self.encoding)
        cipher_bytes = cipher.encrypt(plain_text)
        nonce = base64.b64encode(cipher.nonce).decode(self.encoding)
        cipher_text = base64.b64encode(cipher_bytes).decode(self.encoding)
        return f"{self.escape(cipher_text)}{self._join_string}{self.escape(nonce)}"

    def decrypt(self, encrypted: str) -> str:
        cipher_text, nonce = encrypted.split(self._join_string)
        cipher_text = base64.b64decode(self.un_escape(cipher_text))
        nonce = base64.b64decode(self.un_escape(nonce))
        cipher = _AES.new(key=self.key, mode=self._mode, nonce=nonce)
        plain_text = cipher.decrypt(cipher_text)
        return plain_text.decode(self.encoding)
