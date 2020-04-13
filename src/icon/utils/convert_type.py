# -*- coding: utf-8 -*-
# Copyright 2020 ICON Foundation Inc.
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

from typing import Optional

from ..data.address import Address


def str_to_int(value: str) -> int:
    if isinstance(value, int):
        return value

    base = 16 if is_hex(value) else 10
    return int(value, base)


def object_to_str(value) -> str:
    if isinstance(value, Address):
        return str(value)
    elif isinstance(value, int):
        return hex(value)
    elif isinstance(value, bytes):
        return bytes_to_hex(value)
    elif isinstance(value, bool):
        return "0x1" if value else "0x0"

    return value


def to_str_list(o: list) -> list:
    """Return a copied list from a given list

    All items in the origin list are copied to a copied list and converted in string format
    There is no change in a given list
    """

    ret = []

    for value in o:
        if isinstance(value, dict):
            value = to_str_dict(value)
        elif isinstance(value, list):
            value = to_str_list(value)
        else:
            value = object_to_str(value)

        ret.append(value)

    return ret


def to_str_dict(o: dict) -> dict:
    ret = {}

    for key, value in o.items():
        if isinstance(value, dict):
            value = to_str_dict(value)
        elif isinstance(value, list):
            value = to_str_list(value)
        else:
            value = object_to_str(value)

        ret[key] = value

    return ret


def str_to_object(object_type: str, value: str) -> object:
    if object_type == "Address":
        return Address.from_string(value)
    if object_type == "int":
        return str_to_int(value)
    if object_type == "bytes":
        return hex_to_bytes(value)
    if object_type == "bool":
        return bool(str_to_int(value))
    if object_type == "str":
        return value

    raise TypeError(f"Unknown type: {object_type}")


def bytes_to_hex(value: bytes, prefix: str = "0x") -> str:
    return f"{prefix}{value.hex()}"


def hex_to_bytes(value: Optional[str]) -> Optional[bytes]:
    if value is None:
        return None

    if value.startswith("0x"):
        value = value[2:]

    return bytes.fromhex(value)


def is_hex(value: str) -> bool:
    return value.startswith("0x") or value.startswith("-0x")
