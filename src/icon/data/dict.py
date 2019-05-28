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

__all__ = "Dict"

from collections.abc import MutableMapping
from typing import Union
import json

from ..data.address import Address
from .object import Object
from .primitive import Primitive

_VALUE_TYPES = (bool, int, bytes, str, Address, MutableMapping)


def _check_key_type(key: str):
    if not isinstance(key, str):
        raise TypeError("Invalid key")


def _check_value_type(value: Union[bool, int, bytes, str, Address, MutableMapping]):
    if not isinstance(value, Object):
        TypeError("Invalid type")


class JsonRpcEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Object):
            return str(o)

        return json.JSONEncoder.default(self, o)


class Dict(dict):
    def __init__(self):
        super().__init__()

    def __getitem__(self, key: str):
        _check_key_type(key)
        return super().__getitem__(key)

    def __setitem__(self, key: str, value):
        _check_key_type(key)
        _check_value_type(value)

        super().__setitem__(key, value)

    def __delitem__(self, key: str):
        _check_key_type(key)
        super().__delitem__(key)

    def __str__(self) -> str:
        separators = (",", ":")
        return json.dumps(self, cls=JsonRpcEncoder, separators=separators)

    def __bytes__(self) -> bytes:
        pass

    def to_dict(self) -> dict:
        return self
