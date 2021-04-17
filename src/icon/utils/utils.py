# -*- coding: utf-8 -*-

from base64 import standard_b64encode
from typing import Dict
from .serializer import generate_message_hash
from .crypto import sign


def is_keystore_valid(keystore: dict) -> bool:
    """Checks data in a keystore file is valid.
    :return: type(bool)
        True: When format of the keystore is valid.
        False: When format of the keystore is invalid.
    """

    root_keys = ["version", "id", "address", "crypto", "coinType"]
    crypto_keys = ["ciphertext", "cipherparams", "cipher", "kdf", "kdfparams", "mac"]
    crypto_cipherparams_keys = ["iv"]

    return (
        has_keys(keystore, root_keys)
        and has_keys(keystore["crypto"], crypto_keys)
        and has_keys(keystore["crypto"]["cipherparams"], crypto_cipherparams_keys)
    )


def has_keys(target_data: dict, keys: list):
    """Checks to a target data for having all of keys in list."""
    for key in keys:
        if key not in target_data:
            return False
    return True


def generate_signature(tx: Dict[str, str], private_key: bytes) -> str:
    tx_hash: bytes = generate_message_hash(tx)
    signature: bytes = sign(tx_hash, private_key, recoverable=True)
    return standard_b64encode(signature).decode("utf-8")
