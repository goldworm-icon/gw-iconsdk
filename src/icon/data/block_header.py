# -*- coding: utf-8 -*-
from __future__ import annotations

import hashlib
from typing import Optional

from .address import Address
from .utils import bytes_to_hex
from ..utils import rlp


class BlockHeader:
    def __init__(self, data: bytes):
        self._bytes = data
        self._hash = hashlib.sha3_256(data).digest()

        unpacked = rlp.rlp_decode(
            self._bytes,
            [int, int, int, bytes, bytes, bytes, bytes, bytes, bytes, bytes, bytes]
        )
        # version check
        if unpacked[0] != 2:
            raise Exception("Support Block V2 only")

        (
            self._version,
            self._height,
            self._timestamp,
            proposer,
            self._prev_hash,
            self._votes_hash,
            self._next_validators_hash,
            self._patch_txs_hash,
            self._normal_txs_hash,
            self._logs_bloom,
            result_packed,
        ) = unpacked
        self._proposer = Address.from_bytes(proposer)
        self._result = Result(result_packed)

    def __str__(self):
        text = "\n".join((
            f"version={self._version}",
            f"height={self._height}",
            f"timestamp={self._timestamp}",
            f"proposer={self._proposer}",
            f"prev_hash={bytes_to_hex(self._prev_hash)}",
            f"votes_hash={bytes_to_hex(self._votes_hash)}",
            f"next_validators_hash={bytes_to_hex(self._next_validators_hash)}",
            f"patch_txs_hash={bytes_to_hex(self._patch_txs_hash)}",
            f"normal_txs_hash={bytes_to_hex(self._normal_txs_hash)}",
            f"logs_bloom={bytes_to_hex(self._logs_bloom)}",
        ))
        return f"{text}\n{self._result}"

    @property
    def bytes(self) -> bytes:
        """rlp-encoded block header data
        :return: rlp-encoded bytes
        """
        return self._bytes

    @property
    def hash(self) -> bytes:
        return self._hash

    @property
    def height(self) -> int:
        return self._height

    @property
    def votes_hash(self) -> bytes:
        return self._votes_hash

    @property
    def next_validators_hash(self) -> bytes:
        return self._next_validators_hash

    @property
    def result(self) -> Result:
        return self._result

    @classmethod
    def from_bytes(cls, data: bytes) -> Optional[BlockHeader]:
        if not isinstance(data, bytes) or len(data) < 1:
            return None
        return cls(data)


class Result:
    def __init__(self, data: bytes):
        self._state_hash = None
        self._patch_receipt_hash = None
        self._normal_receipt_hash = None
        self._extension_data = None

        if isinstance(data, bytes) and len(data) > 0:
            (
                self._state_hash,
                self._patch_receipt_hash,
                self._receipt_hash,
                self._extension_data,
            ) = rlp.rlp_decode(data, [bytes, bytes, bytes, bytes])

    def __str__(self):
        return "\n".join((
            f"state_hash={bytes_to_hex(self._state_hash)}",
            f"patch_receipt_hash={bytes_to_hex(self._patch_receipt_hash)}",
            f"normal_receipt_hash={bytes_to_hex(self._normal_receipt_hash)}",
            f"extension_data={bytes_to_hex(self._extension_data)}",
        ))

    @property
    def state_hash(self) -> bytes:
        return self._state_hash

    @property
    def patch_receipt_hash(self) -> bytes:
        return self._patch_receipt_hash

    @property
    def normal_receipt_hash(self) -> bytes:
        return self._normal_receipt_hash

    @property
    def extension_data(self) -> bytes:
        return self._extension_data

    @classmethod
    def from_bytes(cls, bs: bytes) -> Result:
        return cls(bs)
