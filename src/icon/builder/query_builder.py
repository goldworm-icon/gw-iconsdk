# -*- coding: utf-8 -*-

__all__ = "CallBuilder"

from typing import Dict, Optional

from .generic_builder import GenericBuilder
from .key import Key
from ..data.address import Address


class CallBuilder(GenericBuilder):
    def __init__(self):
        super().__init__()
        self.add(Key.DATA_TYPE, "call")

    def from_(self, address: Address) -> "CallBuilder":
        self.add(Key.FROM, address)
        return self

    def to(self, address: Address) -> "CallBuilder":
        self.add(Key.TO, address)
        return self

    def data(self, method: str, params: Optional[Dict[str, str]]) -> "CallBuilder":
        data = {"method": method}
        if isinstance(params, dict):
            data["params"] = params

        self.add(Key.DATA, data)
        return self

    def build(self) -> Dict[str, str]:
        return super().build()
