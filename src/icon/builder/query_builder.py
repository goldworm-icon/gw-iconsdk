# -*- coding: utf-8 -*-

__all__ = "CallBuilder"

from typing import Dict, Any, Optional

from .generic_builder import GenericBuilder
from .key import Key
from ..data.address import Address
from ..data.exception import DataTypeException


class CallBuilder(GenericBuilder):
    def __init__(self, method: str):
        super().__init__()

        self.add(Key.DATA_TYPE, "call")
        self._data: Dict[str, Any] = {"method": method}

    def from_(self, address: Address) -> "CallBuilder":
        self.add(Key.FROM, address)
        return self

    def to(self, address: Address) -> "CallBuilder":
        self.add(Key.TO, address)
        return self

    def method(self, method: str) -> "CallBuilder":
        self._data["method"] = method
        return self

    def params(self, params: Optional[Dict[str, Any]]) -> "CallBuilder":
        if params is None:
            return self

        if not isinstance(params, dict):
            raise DataTypeException(f"params must be dict type: {params}")

        self._data["params"] = params
        return self

    def build(self) -> Dict[str, str]:
        self.add(Key.DATA, self._data)
        return super().build()
