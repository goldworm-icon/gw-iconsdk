# -*- coding: utf-8 -*-

from threading import Lock
from typing import Optional, Dict

from ..builder import Transaction


class RpcRequest(object):
    _next_id = 0
    _id_lock = Lock()

    def __init__(self, method: str, params: Optional[Dict[str, str]] = None):
        self._id = self._get_next_id()
        self._method = method
        self._params = params

    @classmethod
    def _get_next_id(cls) -> int:
        with cls._id_lock:
            _id = cls._next_id
            cls._next_id = (cls._next_id + 1) % 0xFFFFFFFF

        return _id

    @property
    def id(self) -> int:
        return self._id

    @property
    def params(self) -> Optional[Dict[str, str]]:
        return self._params

    @property
    def method(self) -> str:
        return self._method

    def to_dict(self) -> Dict[str, str]:
        ret = {
            "jsonrpc": "2.0",
            "id": self._id,
            "method": self._method,
        }

        if isinstance(self._params, Transaction):
            ret["params"] = self._params.to_dict()
        elif isinstance(self._params, dict):
            ret["params"] = self._params

        return ret
