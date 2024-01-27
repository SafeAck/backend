from os import urandom
from binascii import hexlify


def generate_secret(length: int = 32) -> str:
    return hexlify(urandom(length)).decode()
