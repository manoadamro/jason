from Crypto.Cipher import Salsa20 as _Salsa20


class Salsa20:
    def __init__(self, key):
        self.key = key

    def cipher(self, nonce=None):
        return _Salsa20.new(key=self.key, nonce=nonce)

    def encrypt(self, text: str) -> bytes:
        raise NotImplementedError

    def decrypt(self, text: str) -> str:
        raise NotImplementedError
