# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Tuple

from .address import Address
from ..utils import rlp


class Validators:
    def __init__(self, addresses: Tuple[Address]):
        self._addresses = addresses

    def __len__(self) -> int:
        return len(self._addresses)

    def __contains__(self, address: Address) -> bool:
        return address in self._addresses

    def __str__(self):
        return "\n".join((str(address) for address in self._addresses))

    @property
    def addresses(self) -> Tuple[Address]:
        return self._addresses

    @classmethod
    def from_bytes(cls, bs: bytes) -> Validators:
        unpacked = rlp.rlp_decode(bs, {list: bytes})
        return cls(tuple(Address.from_bytes(item) for item in unpacked))
