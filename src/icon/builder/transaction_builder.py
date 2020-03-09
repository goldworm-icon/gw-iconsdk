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

from typing import TYPE_CHECKING, Union

from ..data.rpc_request import RpcRequest

if TYPE_CHECKING:
    from ..data.address import Address


class TransactionBuilder(object):
    """Helper to make it easy to create a RPC request message

    """

    def __init__(self, method: str):
        self._request = RpcRequest(method)

    def version(self, version: int) -> 'TransactionBuilder':
        return self

    def from_(self, from_: 'Address') -> 'TransactionBuilder':
        return self

    def to(self, to: str) -> 'TransactionBuilder':
        return self

    def value(self, value: int) -> 'TransactionBuilder':
        return self

    def step_limit(self, step_limit: int) -> 'TransactionBuilder':
        return self

    def timestamp(self, timestamp_us: int) -> 'TransactionBuilder':
        return self

    def nid(self, nid: int) -> 'TransactionBuilder':
        return self

    def signature(self, signature: bytes) -> 'TransactionBuilder':
        return self

    def data_type(self, data_type: str) -> 'TransactionBuilder':
        return self

    def data(self, params: Union[dict, str]) -> 'TransactionBuilder':
        return self

    def build(self) -> 'RpcRequest':
        request = self._request
        self._request = None
        return request
