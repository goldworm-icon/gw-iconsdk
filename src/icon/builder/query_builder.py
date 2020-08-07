# -*- coding: utf-8 -*-

__all__ = "CallBuilder"

from typing import Dict, Any

from . import PROTO_VERSION
from .generic_builder import GenericBuilder
from .key import Key
from ..data.address import Address
from ..data.exception import DataTypeException


class CallBuilder(GenericBuilder):
    def __init__(self, method: str):
        super().__init__()

        self.add(Key.VERSION, PROTO_VERSION)
        self.add(Key.DATA_TYPE, "call")

        self._data: Dict[str, Any] = {"method": method}

    def version(self, version: int) -> "CallBuilder":
        self.add(Key.VERSION, version)
        return self

    def from_(self, from_: Address) -> "CallBuilder":
        self.add(Key.FROM, from_)
        return self

    def method(self, method: str) -> "CallBuilder":
        self._data["method"] = method
        return self

    def params(self, params: Dict[str, Any]) -> "CallBuilder":
        if not isinstance(params, dict):
            raise DataTypeException(f"params must be dict type: {params}")

        self._data["params"] = params
        return self

    def build(self) -> Dict[str, str]:
        self.add(Key.DATA, self._data)
        return super().build()
