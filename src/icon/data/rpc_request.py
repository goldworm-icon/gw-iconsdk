# -*- coding: utf-8 -*-

# Copyright 2019 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from threading import Lock
from typing import Optional

from .dict import Dict
from ..utils.convert_type import to_str_dict


class RpcRequest(object):
    _next_id = 0
    _id_lock = Lock()

    def __init__(self, method: str, params: Dict):
        self._id = self._get_next_id()
        self._method = method

        if params is None:
            params = {}
        self._params = params

    @classmethod
    def _get_next_id(cls) -> int:
        with cls._id_lock:
            _id = cls._next_id
            cls._next_id = (cls._next_id + 1) % 0xffffffff

        return _id

    @property
    def id(self) -> int:
        return self._id

    @property
    def params(self) -> Optional[Dict]:
        return self._params

    @property
    def method(self) -> Optional[str]:
        return self._method

    def to_dict(self) -> dict:
        ret = {"method": self._method}

        if self._params:
            ret["params"] = self._params

        ret = to_str_dict(ret)
        ret["jsonrpc"] = "2.0"
        ret["id"] = self._id

        return ret
