from cryptography.fernet import Fernet
from django.conf import settings

__all__ = ["encrypt", "decrypt"]
DEFAULT_CRYPTO_KEY = settings.CRYPTOGRAPHY_KEY


def _encode_to_bytes(data):
    if isinstance(data, (bytearray, bytes)):
        return data
    return bytes(str(data).encode("utf-8"))


def _decode_to_string(data):
    if isinstance(data, (bytearray, bytes)):
        return data.decode()
    return str(data)


def encrypt(data, key=DEFAULT_CRYPTO_KEY):
    f = Fernet(key)
    return _decode_to_string(f.encrypt(_encode_to_bytes(data)))


def decrypt(data, key=DEFAULT_CRYPTO_KEY):
    f = Fernet(key)
    return _decode_to_string(f.decrypt(_encode_to_bytes(data)))
