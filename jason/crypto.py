import re
import base64

from Crypto.Cipher import ChaCha20 as _ChaCha20


class ChaCha20:
    escape = ("-", "%-")

    def __init__(self, key):
        self.key = key.rjust(32).encode("utf8")

    def _escape(self, string):
        return re.sub(self.escape[0], self.escape[1], string)

    def _un_escape(self, string):
        return re.sub(self.escape[1], self.escape[0], string)

    def encrypt(self, plain_text: str) -> str:
        cipher = _ChaCha20.new(key=self.key)
        cipher_bytes = cipher.encrypt(plain_text.encode("utf8"))
        nonce = base64.b64encode(cipher.nonce).decode("utf-8")
        cipher_text = base64.b64encode(cipher_bytes).decode("utf-8")
        return f"{self._escape(cipher_text)}---{self._escape(nonce)}"

    def decrypt(self, encrypted: str) -> str:
        cipher_text, nonce = encrypted.split("---")
        cipher_text = base64.b64decode(self._un_escape(cipher_text))
        nonce = base64.b64decode(self._un_escape(nonce))
        cipher = _ChaCha20.new(key=self.key, nonce=nonce)
        plain_text = cipher.decrypt(cipher_text)
        return plain_text.decode("utf8")
