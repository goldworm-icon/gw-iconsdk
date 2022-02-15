# -*- coding: utf-8 -*-

from __future__ import annotations

import base64
import json
from typing import Dict, List, Union, Optional, Any

from .address import Address
from .transaction import get_transaction, BaseTransaction, Transaction
from ..builder.key import Key
from ..utils import hex_to_bytes, str_to_int, bytes_to_hex


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


def _get_transactions(
    block_dict: Dict[str, Any]
) -> List[Union[BaseTransaction, Transaction]]:
    key = "confirmed_transaction_list"
    return [get_transaction(tx_dict) for tx_dict in block_dict[key]]


def _default(o: Any) -> Any:
    if isinstance(o, bytes):
        return bytes_to_hex(o)
    elif isinstance(o, Address):
        return str(o)
    elif isinstance(o, (BaseTransaction, Transaction)):
        return o.to_dict()

    return o


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
        transactions: List[Transaction],
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
        self._transactions: List[Transaction] = transactions

    def __repr__(self) -> str:
        return json.dumps(self.to_dict(), indent=4, default=_default)

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

    def to_dict(self) -> Dict[str, Any]:
        ret = {
            "version": self._version,
            "height": self._height,
            "block_hash": self._hash,
            "prev_block_hash": self._prev_hash,
            "merkle_tree_root_hash": self._merkle_tree_root_hash,
            "timestamp": self._timestamp,
            "peer_id": self._peer_id,
            "signature": self._signature,
            "transactions": self._transactions,
        }

        if self._next_leader:
            ret["next_leader"] = self._next_leader

        return ret

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Block:
        print(data)

        version: str = data[Key.VERSION]
        height: int = str_to_int(data["height"])
        block_hash: bytes = hex_to_bytes(data["block_hash"])
        prev_block_hash: bytes = hex_to_bytes(data["prev_block_hash"])
        merkle_tree_root_hash: bytes = hex_to_bytes(data["merkle_tree_root_hash"])
        timestamp: int = _get_timestamp(data)
        peer_id: Address = Address.from_string(data["peer_id"])
        next_leader: Optional[Address] = _get_next_leader(data)
        signature: bytes = _get_signature(data)
        transactions: List[Transaction] = _get_transactions(data)

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
            transactions=transactions,
        )
