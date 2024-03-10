# -*- coding: utf-8 -*-

__all__ = ("sign", "verify_signature", "create_key_pair", "extract_public_key")

from typing import (
    Optional,
    Tuple,
)

import coincurve


def sign(message_hash: bytes, private_key: bytes, recoverable: bool) -> bytes:
    """
    Generates on the ECDSA-SHA256 signature in bytes from data.
    It refers to a document on https://github.com/ludbb/secp256k1-py.

    :param message_hash: 32-byte message_hash to sign
    :param private_key: private key
    :param recoverable: True means that public_key can be recovered from signature and message_hash
    :return signature: signature made from input data
    """
    private_key_object = coincurve.PrivateKey(private_key)

    if recoverable:
        return private_key_object.sign_recoverable(message_hash, hasher=None)
    else:
        return private_key_object.sign(message_hash, hasher=None)


def recover_key(msg_hash: bytes, signature: bytes, compressed: bool = True) -> Optional[bytes]:
    if isinstance(msg_hash, bytes) \
            and len(msg_hash) == 32 \
            and isinstance(signature, bytes) \
            and len(signature) == 65:
        return coincurve.PublicKey.from_signature_and_message(signature, msg_hash, hasher=None).format(compressed)

    return None


def verify_signature(signature: bytes, message_hash: bytes, public_key: bytes) -> bool:
    recoverable: bool = is_signature_recoverable(signature)
    public_key_object = coincurve.PublicKey(public_key)

    if recoverable:
        public_key_object_from_signature = coincurve.PublicKey.from_signature_and_message(
            signature, message_hash, hasher=None
        )
        return public_key_object == public_key_object_from_signature
    else:
        public_key_object.verify(signature, message_hash, hasher=None)


def is_signature_recoverable(signature: bytes) -> bool:
    return isinstance(signature, bytes) and len(signature) == 65


def create_key_pair(
    private_key: bytes = None, compressed: bool = False
) -> Tuple[bytes, bytes]:
    """Return private key and public key pair

    :param private_key:
    :param compressed: The format of a public key to create
    :return: (private_key, uncompressed public_key)
    """
    private_key_object = coincurve.PrivateKey(private_key)

    private_key: bytes = private_key_object.secret
    public_key: bytes = private_key_object.public_key.format(compressed)

    return private_key, public_key


def change_public_key_format(public_key: bytes, compressed: bool) -> bytes:
    public_key_object = coincurve.PublicKey(public_key)
    return public_key_object.format(compressed)


def extract_public_key(private_key: bytes, compressed: bool = False) -> bytes:
    private_key_object = coincurve.PrivateKey(private_key)
    return private_key_object.public_key.format(compressed)
