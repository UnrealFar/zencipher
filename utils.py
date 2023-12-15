import bcrypt
from cryptography.fernet import Fernet

import hashlib
import base64
import os

PUB_KEY = os.environ["PUB_KEY"]
fer = Fernet(PUB_KEY.encode())


def key_from_password(password, salt):
    key = bcrypt.kdf(
        password=password.encode(), salt=salt, desired_key_bytes=32, rounds=100
    )
    key = base64.urlsafe_b64encode(key)
    return key.decode()


def hash_password(password, salt):
    return bcrypt.hashpw(
        base64.b64encode(hashlib.sha256(password.encode()).digest()), salt
    ).decode()


def check_password(password, hashed):
    return bcrypt.checkpw(
        base64.b64encode(hashlib.sha256(password.encode()).digest()), hashed.encode()
    )


def encrypt(s: str, key) -> bytes:
    e = fer.encrypt(s.encode())
    e = Fernet(key).encrypt(e)
    return e


def decrypt(s: bytes, key) -> str:
    d = Fernet(key).decrypt(s)
    d = fer.decrypt(d).decode()
    return d
