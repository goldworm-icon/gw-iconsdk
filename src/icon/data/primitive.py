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

from abc import abstractmethod
from typing import Union

from .object import Object


class Primitive(Object):
    def __init__(self, cls: type, value: Union[bool, int, bytes]):
        self._cls = cls
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, _value):
        if not isinstance(_value, self._cls):
            raise TypeError("Invalid type")

        self._value = _value

    @abstractmethod
    def __str__(self):
        pass


class Bool(Primitive):
    def __init__(self, value: bool):
        super().__init__(bool, value)

    def __str__(self) -> str:
        return hex(self.value)


class Bytes(Primitive):
    def __init__(self, value: bytes):
        super().__init__(bytes, value)

    def __str__(self) -> str:
        return f"0x{self.value.hex()}"


class Int(Primitive):
    def __init__(self, value: int):
        super().__init__(int, value)

    def __str__(self) -> str:
        return hex(self.value)

    def __int__(self) -> int:
        return self.value
