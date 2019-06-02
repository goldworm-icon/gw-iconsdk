# -*- coding: utf-8 -*-

import hashlib
from icon.utils import crypto, crypto2


def test_create_key_pair():
    secp256k1_private_key, secp256k1_public_key = \
        crypto.create_key_pair(private_key=None, compressed=False)
    coincurve_private_key, coincurve_public_key = crypto2.create_key_pair(secp256k1_private_key)

    private_keys = [secp256k1_private_key, coincurve_private_key]
    public_keys = [secp256k1_public_key, coincurve_public_key]

    for i in range(len(private_keys)):
        private_key: bytes = private_keys[i]
        public_key: bytes = public_keys[i]

        assert isinstance(public_key, bytes)
        assert isinstance(public_key, bytes)
        assert len(private_key) == 32
        assert len(public_key) == 65
        assert public_key[0] == 0x04

    assert secp256k1_private_key == coincurve_private_key
    assert secp256k1_public_key == coincurve_public_key


def test_sign_recoverable():
    coincurve_private_key, coincurve_public_key = \
        crypto2.create_key_pair(private_key=None, compressed=False)
    print(coincurve_private_key, coincurve_public_key)
    secp256k1_private_key, secp256k1_public_key = \
        crypto.create_key_pair(coincurve_private_key)

    assert secp256k1_private_key == coincurve_private_key
    assert secp256k1_public_key == coincurve_public_key

    message: bytes = hashlib.sha3_256(b"hello").digest()

    secp256k1_recoverable_sign: bytes = \
        crypto.sign_recoverable(message, secp256k1_private_key)
    coincurve_recoverable_sign: bytes = \
        crypto2.sign_recoverable(message, secp256k1_private_key)

    assert isinstance(secp256k1_recoverable_sign, bytes)
    assert isinstance(coincurve_recoverable_sign, bytes)
    assert secp256k1_recoverable_sign == coincurve_recoverable_sign
