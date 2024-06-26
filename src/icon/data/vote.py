# -*- coding: utf-8 -*-
from __future__ import annotations

import hashlib
from enum import IntEnum
from typing import (
    List,
    Optional,
    Tuple,
)

from .address import Address
from ..utils import (
    bytes_to_hex,
    crypto,
    rlp,
)


class VoteType(IntEnum):
    PREVOTE = 0
    PRECOMMIT = 1


class VoteItem:
    def __init__(self, timestamp: int, signature: bytes):
        self._timestamp = timestamp
        self._signature = signature

    def __str__(self):
        return "\n".join((
            f"timestamp={self._timestamp}",
            f"signature={bytes_to_hex(self._signature)}",
        ))

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def signature(self) -> bytes:
        return self._signature


class PartSetID:
    def __init__(self, count: int, _hash: Optional[bytes]):
        self._count = count
        self._hash = _hash

    def __str__(self):
        return f"[count={self._count} hash={bytes_to_hex(self._hash)}]"

    @property
    def count(self) -> int:
        return self._count

    @property
    def hash(self) -> bytes:
        return self._hash

    @classmethod
    def from_bytes(cls, bs: bytes) -> PartSetID:
        unpacked = rlp.rlp_decode(bs, [int, bytes])
        return cls(unpacked[0], unpacked[1])


class Votes:
    def __init__(self, data: bytes):
        unpacked = rlp.rlp_decode(data, [int, [int, bytes], {list: [int, bytes]}])

        self._bytes = data
        self._round = unpacked[0]
        self._part_set_id = PartSetID(*unpacked[1])
        self._vote_items = tuple(
            VoteItem(*vote_item_data)
            for vote_item_data in unpacked[2]
        )

    def __bytes__(self) -> bytes:
        return self._bytes

    def __str__(self):
        vote_items: str = "\n".join((
            str(item) for item in self._vote_items
        ))
        return "\n".join((
            f"round={self._round}",
            f"part_set_id={self._part_set_id}",
            f"vote_items=[{vote_items}]",
        ))

    def __eq__(self, other):
        return self._bytes == bytes(other)

    @property
    def round(self) -> int:
        return self._round

    @property
    def part_set_id(self) -> PartSetID:
        return self._part_set_id

    @property
    def vote_items(self) -> Tuple[VoteItem]:
        return self._vote_items

    def get_addresses(self, height: int, block_id: bytes) -> List[Address]:
        return get_voters(self, height, block_id)

    @classmethod
    def from_bytes(cls, bs: bytes) -> Optional[Votes]:
        if not isinstance(bs, bytes) or len(bs) < 1:
            return None
        return cls(bs)


def get_voters(votes: Votes, height: int, block_id: bytes) -> List[Address]:
    # validation signature
    vote_msg = [
        height,
        votes.round,
        VoteType.PRECOMMIT.value,
        block_id,
        [votes.part_set_id.count, votes.part_set_id.hash],
    ]

    voters = []
    for vote_item in votes.vote_items:
        vote_msg.append(vote_item.timestamp)
        serialized_vote_msg = rlp.rlp_encode(vote_msg)
        msg_hash = hashlib.sha3_256(serialized_vote_msg).digest()
        public_key = crypto.recover_key(msg_hash, vote_item.signature, False)
        voters.append(Address.from_public_key(public_key))
        # Remove voteItem timestamp from vote_msg
        vote_msg.pop()
    return voters
