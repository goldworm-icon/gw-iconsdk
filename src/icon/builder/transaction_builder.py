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
    "Transaction",
    "TransactionBuilder",
    "CallTransactionBuilder",
    "DeployTransactionBuilder",
)

from base64 import standard_b64encode
from collections import Mapping
from time import time_ns
from typing import Union, Dict, Any, Optional, Iterator

from .generic_builder import GenericBuilder
from .key import Key, KeyFlag
from ..data.address import Address
from icon.exception import CallException, DataTypeException
from ..utils.crypto import sign
from ..utils.in_memory_zip import gen_deploy_data_content
from ..utils.serializer import generate_message_hash

PROTO_VERSION = 3


class Transaction(Mapping):
    def __init__(self, params: Dict[str, str]):
        super().__init__()
        self._hash: bytes = generate_message_hash(params)
        self._params = params

    def __getitem__(self, k: str) -> str:
        return self._params.__getitem__(k)

    def __len__(self) -> int:
        return self._params.__len__()

    def __iter__(self) -> Iterator[str]:
        return self._params.__iter__()

    @property
    def tx_hash(self) -> bytes:
        return self._hash

    def sign(self, private_key: bytes) -> Optional[bytes]:
        if Key.SIGNATURE in self._params:
            return None

        signature: bytes = sign(self._hash, private_key, recoverable=True)
        self._params[Key.SIGNATURE] = standard_b64encode(signature).decode("utf-8")
        return signature

    def to_dict(self) -> Dict[str, str]:
        return self._params


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

    def nonce(self, nonce: int) -> "TransactionBuilder":
        self.add(Key.NONCE, nonce)
        self._set_flag(KeyFlag.NONCE, True)
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

    def build(self) -> Transaction:
        if Key.TIMESTAMP not in self._params:
            time_us = time_ns() * 1000
            self.timestamp(time_us)

        params: Dict[str, str] = super().build()
        return Transaction(params)


class CallTransactionBuilder(TransactionBuilder):
    def __init__(self):
        super().__init__()

    def data(self, data: Union[Dict[str, Any], str]):
        raise CallException(f"data() is not allowed in {self.__class__.__name__}")

    def call_data(
        self, method: str, params: Optional[Dict[str, str]]
    ) -> "CallTransactionBuilder":
        data = {"method": method}
        if isinstance(params, dict):
            data["params"] = params

        super().data_type("call")
        super().data(data)
        return self


class DeployTransactionBuilder(TransactionBuilder):
    def __init__(self):
        super().__init__()

    def data(self, data: Union[Dict[str, Any], str]):
        raise CallException(f"data() is not allowed in {self.__class__.__name__}")

    def deploy_data_from_bytes(
        self, data: bytes, params: Optional[Dict[str, Any]]
    ) -> "DeployTransactionBuilder":
        deploy_data = {"content": data, "contentType": "application/zip"}

        if params:
            if not isinstance(params, dict):
                raise DataTypeException(f"params must be dict type: {params}")

            deploy_data["params"] = params

        super().data_type("deploy")
        super().data(deploy_data)
        return self

    def deploy_data_from_path(
        self, path: str, params: Optional[Dict[str, Any]]
    ) -> "DeployTransactionBuilder":
        data: bytes = gen_deploy_data_content(path)
        return self.deploy_data_from_bytes(data, params)
