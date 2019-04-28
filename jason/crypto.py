from base64 import b64decode, b64encode

from Crypto.Cipher import ChaCha20 as _ChaCha20


class ChaCha20:
    def __init__(self, key):
        self.key = key.rjust(32).encode("utf8")

    def encrypt(self, plain_text: str) -> str:
        cipher = _ChaCha20.new(key=self.key)
        cipher_bytes = cipher.encrypt(plain_text.encode("utf8"))
        nonce = b64encode(cipher.nonce).decode("utf-8")
        cipher_text = b64encode(cipher_bytes).decode("utf-8")
        # TODO escape '-' character in nonce
        # TODO escape '-' character in cipher_text
        return f"{cipher_text}---{nonce}"

    def decrypt(self, encrypted: str) -> str:
        cipher_text, nonce = encrypted.split("---")
        # TODO unescape '-' character in nonce
        # TODO unescape '-' character in cipher_text
        cipher_text = b64decode(cipher_text)
        nonce = b64decode(nonce)
        cipher = _ChaCha20.new(key=self.key, nonce=nonce)
        plain_text = cipher.decrypt(cipher_text)
        return plain_text.decode("utf8")
