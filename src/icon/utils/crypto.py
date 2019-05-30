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

__all__ = ("sign", "create_key_pair", "extract_public_key")

from secp256k1 import PrivateKey
from typing import Tuple

_private_key_object = PrivateKey()
_ctx = _private_key_object.ctx


def sign(data: bytes, private_key: bytes) -> bytes:
    """
    Generates on the ECDSA-SHA256 signature in bytes from data.
    It refers to a document on https://github.com/ludbb/secp256k1-py.

    :param data: data to be signed
    :param private_key: private key
    :return signature: signature made from input data
    """
    private_key_object = PrivateKey(private_key, raw=True, ctx=_ctx)
    recoverable_sign = private_key_object.ecdsa_sign_recoverable(data, raw=True)
    sign_bytes, sign_recovery = private_key_object.ecdsa_recoverable_serialize(recoverable_sign)
    return sign_bytes + sign_recovery.to_bytes(1, 'big')


def create_key_pair(private_key: bytes = None) -> Tuple[bytes, bytes]:
    """

    :param private_key:
    :return: (private_key, uncompressed public_key)
    """
    private_key_object = PrivateKey(private_key, raw=True, ctx=_ctx)

    private_key: bytes = private_key_object.private_key
    public_key: bytes = private_key_object.pubkey.serialize(compressed=False)

    return private_key, public_key


def extract_public_key(private_key: bytes, compressed: bool = False) -> bytes:
    private_key_object = PrivateKey(private_key, raw=True, ctx=_ctx)
    return private_key_object.pubkey.serialize(compressed=compressed)
