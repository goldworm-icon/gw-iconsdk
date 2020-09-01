# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Dict, Optional, Any

from .generic_builder import GenericBuilder
from .key import Key
from ..data.address import Address


class CallBuilder(GenericBuilder):
    def __init__(self):
        super().__init__()

    def from_(self, address: Address) -> CallBuilder:
        self.add(Key.FROM, address)
        return self

    def to(self, address: Address) -> CallBuilder:
        self.add(Key.TO, address)
        return self

    def call_data(self, method: str, params: Optional[Dict[str, Any]]) -> CallBuilder:
        data = {"method": method}
        if isinstance(params, dict):
            data["params"] = params

        self.add(Key.DATA_TYPE, "call")
        self.add(Key.DATA, data)
        return self

    def build(self) -> Dict[str, str]:
        return super().build()
