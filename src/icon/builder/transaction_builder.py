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

__all__ = (
    "TransactionBuilder",
    "CallTransactionBuilder",
    "DeployTransactionBuilder"
)

from base64 import standard_b64encode
from time import time_ns
from typing import Union, Dict, Any, Optional

from . import PROTO_VERSION
from .generic_builder import GenericBuilder
from .key import Key, KeyFlag
from ..data.address import Address
from ..data.exception import CallException, DataTypeException
from ..utils.crypto2 import sign_recoverable
from ..utils.in_memory_zip import gen_deploy_data_content
from ..utils.serializer import generate_message, generate_message_hash


class TransactionBuilder(GenericBuilder):
    """Helper to make it easy to create a RPC request message

    """

    def __init__(self):
        super().__init__()
        self._flags: KeyFlag = KeyFlag.NONE

        self.version(PROTO_VERSION)

    def _set_flag(self, flag: KeyFlag, on: bool):
        if on:
            self._flags |= flag
        else:
            self._flags &= ~flag

    def version(self, version: int) -> "TransactionBuilder":
        self.add(Key.VERSION, version)
        self._set_flag(KeyFlag.VERSION, True)
        return self

    def from_(self, from_: Address) -> "TransactionBuilder":
        self.add(Key.FROM, from_)
        self._set_flag(KeyFlag.FROM, True)
        return self

    def to(self, to: Address) -> "TransactionBuilder":
        self.add(Key.TO, to)
        self._set_flag(KeyFlag.TO, True)
        return self

    def value(self, value: int) -> "TransactionBuilder":
        self.add(Key.VALUE, value)
        self._set_flag(KeyFlag.VALUE, True)
        return self

    def step_limit(self, step_limit: int) -> "TransactionBuilder":
        self.add(Key.STEP_LIMIT, step_limit)
        self._set_flag(KeyFlag.STEP_LIMIT, True)
        return self

    def timestamp(self, timestamp_us: int) -> "TransactionBuilder":
        self.add(Key.TIMESTAMP, timestamp_us)
        self._set_flag(KeyFlag.TIMESTAMP, True)
        return self

    def nid(self, nid: int) -> "TransactionBuilder":
        self.add(Key.NID, nid)
        self._set_flag(KeyFlag.NID, True)
        return self

    def signature(self, signature: bytes) -> "TransactionBuilder":
        self.add(Key.SIGNATURE, signature)
        self._set_flag(KeyFlag.SIGNATURE, True)
        return self

    def data_type(self, data_type: str) -> "TransactionBuilder":
        self.add(Key.DATA_TYPE, data_type)
        self._set_flag(KeyFlag.DATA_TYPE, True)
        return self

    def data(self, data: Union[Dict[str, Any], str]) -> "TransactionBuilder":
        self.add(Key.DATA, data)
        self._set_flag(KeyFlag.DATA, True)
        return self

    def generate_message(self) -> str:
        return generate_message(self._params)

    def generate_message_hash(self) -> bytes:
        return generate_message_hash(self._params)

    def build_and_sign(self, private_key: bytes) -> Dict[str, str]:
        if Key.TIMESTAMP not in self._params:
            time_us = time_ns() * 1000
            self.timestamp(time_us)

        params: Dict[str, str] = super().build()

        if Key.SIGNATURE not in params:
            params[Key.SIGNATURE] = self._sign(private_key, params)

        return params

    @classmethod
    def _sign(cls, private_key: bytes, params: Dict[str, str]) -> Optional[str]:
        message_hash: bytes = generate_message_hash(params)
        sign: bytes = sign_recoverable(message_hash, private_key)
        return standard_b64encode(sign).decode("utf-8")


class CallTransactionBuilder(TransactionBuilder):
    def __init__(self, method: str):
        super().__init__()
        super().data_type("call")
        self._data: Dict[str, Any] = {"method": method}

    def data(self, data: Union[Dict[str, Any], str]):
        raise CallException(f"data() is not allowed in {self.__class__.__name__}")

    def method(self, method: str) -> "CallTransactionBuilder":
        self._data["method"] = method
        return self

    def params(self, params: Dict[str, Any]) -> "CallTransactionBuilder":
        if not isinstance(params, dict):
            raise DataTypeException(f"params must be dict type: {params}")

        self._data["params"] = params
        return self

    def build_and_sign(self, private_key: bytes) -> Dict[str, str]:
        super().data(self._data)
        return super().build_and_sign(private_key)


class DeployTransactionBuilder(TransactionBuilder):
    def __init__(self):
        super().__init__()
        super().data_type("deploy")
        self._data: Dict[str, Any] = {}

    def data(self, data: Union[Dict[str, Any], str]):
        raise CallException(f"data() is not allowed in {self.__class__.__name__}")

    def content_from_bytes(self, data: bytes) -> "DeployTransactionBuilder":
        self._data["content"] = data
        self._data["contentType"] = "application/zip"
        return self

    def content_from_path(self, path: str) -> "DeployTransactionBuilder":
        data: bytes = gen_deploy_data_content(path)
        return self.content_from_bytes(data)

    def params(self, params: Dict[str, Any]) -> "DeployTransactionBuilder":
        if not isinstance(params, dict):
            raise DataTypeException(f"params must be dict type: {params}")

        self._data["params"] = params
        return self

    def build_and_sign(self, private_key: bytes) -> Dict[str, str]:
        super().data(self._data)
        return super().build()
