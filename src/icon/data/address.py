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

"""functions and classes to handle address
"""

from enum import IntEnum
import hashlib

from .object import Object

_EOA_PREFIX = "hx"
_CONTRACT_PREFIX = "cx"


class AddressPrefix(IntEnum):
    """
    Enumeration of Address prefix

    - CONTRACT: Contract Account
    - EOA: Externally Owned Account
    """

    EOA = 0
    CONTRACT = 1

    def __str__(self) -> str:
        if self == AddressPrefix.EOA:
            return _EOA_PREFIX
        if self == AddressPrefix.CONTRACT:
            return _CONTRACT_PREFIX

    @staticmethod
    def from_string(prefix: str) -> "AddressPrefix":
        """
        Returns address prefix enumerator

        :param prefix: 2-byte address prefix (hx or cx)
        :return: (AddressPrefix) address prefix enumerator
        """
        if not isinstance(prefix, str):
            raise TypeError(f"Invalid type: {type(prefix)}")

        if prefix == _EOA_PREFIX:
            return AddressPrefix.EOA
        if prefix == _CONTRACT_PREFIX:
            return AddressPrefix.CONTRACT

        raise ValueError(f"Invalid prefix: {prefix}")


class Address(Object):
    """Address class
    """

    def __init__(self, prefix: AddressPrefix, body: bytes):
        """Constructor

        :param prefix: address prefix enumerator
        :param body: 20-byte address body
        """

        if not isinstance(prefix, AddressPrefix):
            raise TypeError("Invalid prefix")
        if not isinstance(body, bytes):
            raise TypeError("Invalid body")
        if len(body) != 20:
            raise ValueError("Invalid body")

        self._prefix = prefix
        self._body = body

    @property
    def prefix(self) -> AddressPrefix:
        """Returns address prefix part

        :return: :class:`.AddressPrefix` AddressPrefix.EOA(0) or AddressPrefix.CONTRACT(1)
        """
        return self._prefix

    @property
    def body(self) -> bytes:
        """Returns 20-byte address body part

        :return: 20 byte data standing for address
        """
        return self._body

    def __eq__(self, other) -> bool:
        """operator == overriding

        :return: bool
        """
        return \
            isinstance(other, Address) \
            and self._prefix == other.prefix \
            and self._body == other.body

    def __ne__(self, other) -> bool:
        """operator != overriding

        :return: (bool)
        """
        return not self.__eq__(other)

    def __str__(self) -> str:
        """operator str() overriding

        returns prefix(2) + 40-char hexadecimal address

        :return: (str) 42-char address
        """
        return f"{str(self.prefix)}{self.body.hex()}"

    @property
    def is_contract(self) -> bool:
        """
        Whether the address is SCORE

        :return: True(contract) False(Not contract)
        """
        return self._prefix is AddressPrefix.CONTRACT

    @staticmethod
    def from_string(address: str) -> "Address":
        """
        creates an address object from given 42-char string `address`

        :return: :class:`.Address`
        """
        if not isinstance(address, str):
            raise TypeError("Invalid address")
        if len(address) != 42:
            raise ValueError("Invalid address")

        prefix = AddressPrefix.from_string(address[:2])
        body = bytes.fromhex(address[2:])

        return Address(prefix, body)

    @staticmethod
    def from_public_key(public_key: bytes) -> "Address":
        if not isinstance(public_key, bytes):
            raise TypeError("Invalid type")
        if not (len(public_key) == 65 and public_key[0] == 0x04):
            raise ValueError("Invalid value")

        body: bytes = hashlib.sha3_256(public_key[1:]).digest()[-20:]
        return Address(AddressPrefix.EOA, body)
