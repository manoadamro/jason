import base64

from Crypto.Cipher import AES


class Cipher:
    def __init__(self, key):
        self.key = key.rjust(16).encode("utf8")

    def encrypt(self, plaintext: str) -> bytes:
        cipher = AES.new(
            self.key, AES.MODE_ECB
        )  # never use ECB in strong systems obviously
        plaintext += "0" * (16 - (len(plaintext) % 16))
        to_encrypt = plaintext.encode("utf8")
        encoded = base64.b64encode(cipher.encrypt(to_encrypt))
        return encoded

    def decrypt(self, ciphertext: str) -> str:
        cipher = AES.new(
            self.key, AES.MODE_ECB
        )  # never use ECB in strong systems obviously
        to_decrypt = base64.b64decode(ciphertext)
        decoded = cipher.decrypt(to_decrypt)
        return decoded.decode("utf8").strip()
