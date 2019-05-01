import base64
import re

from Crypto.Cipher import ChaCha20 as _ChaCha20


class ChaCha20:
    encoding = "utf8"
    join_char = "-"
    join_string = join_char * 2
    key_length = 32
    escape = (join_char, f"%{join_char}")

    def __init__(self, key):
        key = key.rjust(self.key_length)
        self.key = key.encode(self.encoding)

    def _escape(self, string):
        return re.sub(self.escape[0], self.escape[1], string)

    def _un_escape(self, string):
        return re.sub(self.escape[1], self.escape[0], string)

    def encrypt(self, plain_text: str) -> str:
        cipher = _ChaCha20.new(key=self.key)
        cipher_bytes = cipher.encrypt(plain_text.encode(self.encoding))
        nonce = base64.b64encode(cipher.nonce).decode(self.encoding)
        cipher_text = base64.b64encode(cipher_bytes).decode(self.encoding)
        return f"{self._escape(cipher_text)}{self.join_string}{self._escape(nonce)}"

    def decrypt(self, encrypted: str) -> str:
        cipher_text, nonce = encrypted.split(self.join_string)
        cipher_text = base64.b64decode(self._un_escape(cipher_text))
        nonce = base64.b64decode(self._un_escape(nonce))
        cipher = _ChaCha20.new(key=self.key, nonce=nonce)
        plain_text = cipher.decrypt(cipher_text)
        return plain_text.decode(self.encoding)
