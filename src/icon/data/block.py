# -*- coding: utf-8 -*-

import base64
from typing import Dict, List, Union, Optional

from .address import Address
from .transaction import Transaction
from ..builder.key import Key
from icon.data.utils import hex_to_bytes, str_to_int, bytes_to_hex


def _get_timestamp(block_dict: dict) -> int:
    keys = ["timestamp", "time_stamp"]

    for key in keys:
        if key in block_dict:
            timestamp: Union[int, str] = block_dict[key]
            if isinstance(timestamp, str):
                timestamp = str_to_int(timestamp)

            return timestamp


def _get_next_leader(block_dict: dict) -> Optional[Address]:
    value = block_dict.get("next_leader")
    if value:
        value = Address.from_string(value)

    return value


def _get_signature(block_dict: dict) -> bytes:
    # value is a base64-encoded signature
    value: str = block_dict["signature"]
    return base64.standard_b64decode(value)


class Block(object):
    """Represents block information from

    """

    def __init__(
        self,
        *,
        version: str,
        height: int,
        block_hash: bytes,
        prev_block_hash: bytes,
        timestamp: int,
        merkle_tree_root_hash: bytes,
        peer_id: Address,
        next_leader: Optional[Address],
        signature: bytes,
    ):
        self._version: str = version
        self._height: int = height
        self._hash: bytes = block_hash
        self._prev_hash: bytes = prev_block_hash
        self._timestamp: int = timestamp
        self._merkle_tree_root_hash: bytes = merkle_tree_root_hash
        self._peer_id: Address = peer_id
        self._next_leader: Optional[Address] = next_leader
        self._signature: bytes = signature
        self._transactions: List[Transaction] = []

    def __str__(self) -> str:
        items = (
            f"version={self._version}",
            f"height={self._height}",
            f"hash={bytes_to_hex(self._hash)}",
            f"prev_hash={bytes_to_hex(self._prev_hash)}",
            f"timestamp={self._timestamp}",
            f"merkle_tree_root_hash={bytes_to_hex(self._merkle_tree_root_hash)}",
            f"peer_id={self._peer_id}",
            f"next_leader={self.next_leader}",
            f"signature={bytes_to_hex(self._signature)}",
            f"transactions={self._transactions}",
        )

        return "\n".join(items)

    @property
    def version(self) -> str:
        return self._version

    @property
    def height(self) -> int:
        return self._height

    @property
    def block_hash(self) -> bytes:
        return self._hash

    @property
    def prev_block_hash(self) -> bytes:
        return self._prev_hash

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def merkle_tree_root_hash(self) -> bytes:
        return self._merkle_tree_root_hash

    @property
    def peer_id(self) -> Address:
        return self._peer_id

    @property
    def next_leader(self) -> Optional[Address]:
        return self._next_leader

    @property
    def signature(self) -> bytes:
        return self._signature

    @property
    def transactions(self) -> List[Transaction]:
        return self._transactions

    @classmethod
    def from_dict(cls, data: Dict) -> "Block":
        version: str = data[Key.VERSION]
        height: int = str_to_int(data["height"])
        block_hash: bytes = hex_to_bytes(data["block_hash"])
        prev_block_hash: bytes = hex_to_bytes(data["prev_block_hash"])
        merkle_tree_root_hash: bytes = hex_to_bytes(data["merkle_tree_root_hash"])
        timestamp: int = _get_timestamp(data)
        peer_id: Address = Address.from_string(data["peer_id"])
        next_leader: Optional[Address] = _get_next_leader(data)
        signature: bytes = _get_signature(data)

        return cls(
            version=version,
            height=height,
            block_hash=block_hash,
            prev_block_hash=prev_block_hash,
            timestamp=timestamp,
            merkle_tree_root_hash=merkle_tree_root_hash,
            peer_id=peer_id,
            next_leader=next_leader,
            signature=signature,
        )
