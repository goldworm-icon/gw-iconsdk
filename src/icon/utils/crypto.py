# -*- coding: utf-8 -*-
# Copyright 2018 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__all__ = ("sign", "verify_signature", "create_key_pair", "extract_public_key")

from typing import Tuple

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
    """

    :param private_key:
    :param compressed: The format of a public key to create
    :return: (private_key, uncompressed public_key)
    """
    private_key_object = coincurve.PrivateKey(private_key)

    private_key: bytes = private_key_object.secret
    public_key: bytes = private_key_object.public_key.format(compressed)

    return private_key, public_key


def extract_public_key(private_key: bytes, compressed: bool = False) -> bytes:
    private_key_object = coincurve.PrivateKey(private_key)
    return private_key_object.public_key.format(compressed)
