# -*- coding: utf-8 -*-
# Copyright 2020 ICON Foundation
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

from __future__ import annotations

import json
from typing import List, Dict, Tuple, Union, Any

from .address import Address
from ..utils import (
    bytes_to_hex,
    str_to_base_object_by_typename,
)


def _default(o: Any) -> str:
    if isinstance(o, Address):
        return str(o)
    elif isinstance(o, bytes):
        return bytes_to_hex(o)

    return o


class EventLog(object):
    def __init__(self, score_address: Address, indexed: List, data: List):
        self._score_address: Address = score_address
        self._indexed = indexed
        self._data = data

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4, default=_default)

    @property
    def signature(self) -> str:
        return self._indexed[0]

    @property
    def score_address(self) -> Address:
        return self._score_address

    @property
    def indexed(self) -> List[Union[Address, int, str]]:
        return self._indexed

    @property
    def data(self) -> List[Union[Address, int, str]]:
        return self._data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scoreAddress": self._score_address,
            "indexed": self._indexed,
            "data": self._data,
        }

    @classmethod
    def from_dict(cls, event_log: Dict) -> EventLog:
        score_address = Address.from_string(event_log["scoreAddress"])
        indexed = event_log["indexed"]
        data = event_log["data"]

        signature = indexed[0]
        name, types = cls.parse_signature(signature)

        index = 0

        # Convert indexed data type
        for i in range(1, len(indexed)):
            indexed[i] = str_to_base_object_by_typename(types[index], indexed[i])
            index += 1

        # Convert not-indexed data type
        for i in range(len(data)):
            data[i] = str_to_base_object_by_typename(types[index], data[i])
            index += 1

        return EventLog(score_address, indexed, data)

    @classmethod
    def parse_signature(cls, signature: str) -> Tuple[str, List[str]]:
        if signature == "ICXBurned":
            signature = "ICXBurned(int)"

        index = signature.index("(")
        name = signature[:index]
        params = signature[index + 1: -1].split(",")

        return name, params
