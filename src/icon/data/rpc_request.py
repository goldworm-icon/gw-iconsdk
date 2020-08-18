# -*- coding: utf-8 -*-

import random
from threading import Lock
from typing import Optional, Dict, Any


_MAX_ID = 0x7FFFFFFF


class RpcRequest(object):
    _next_id = random.randint(0, _MAX_ID)
    _id_lock = Lock()

    def __init__(self, method: str, params: Optional[Dict[str, Any]] = None):
        self._id = self._get_next_id()
        self._url = ""
        self._method = method
        self._params = params
        self._user_data = None

    @classmethod
    def _get_next_id(cls) -> int:
        with cls._id_lock:
            _id = cls._next_id
            cls._next_id = (cls._next_id + 1) % _MAX_ID

        return _id

    @property
    def id(self) -> int:
        return self._id

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = value

    @property
    def params(self) -> Optional[Dict[str, str]]:
        return self._params

    @property
    def method(self) -> str:
        return self._method

    @property
    def user_data(self) -> Any:
        return self._user_data

    @user_data.setter
    def user_data(self, value: Any):
        self._user_data = value

    def to_dict(self) -> Dict[str, str]:
        ret = {
            "jsonrpc": "2.0",
            "id": self._id,
            "method": self._method,
        }

        if self._params:
            ret["params"] = self._params

        return ret
