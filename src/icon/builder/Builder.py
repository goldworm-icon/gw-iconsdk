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

from typing import Union

from ..data.rpc_request import RpcRequest


class Builder(object):
    """Helper to make it easy to create a RPC request message

    """

    def __init__(self, method: str):
        self._request = RpcRequest(method)

    def method(self, method: str) -> 'Builder':
        return self

    def version(self, version: int) -> 'Builder':
        return self

    def from_(self, from_: str) -> 'Builder':
        return self

    def to(self, to: str) -> 'Builder':
        return self

    def value(self, value: int) -> 'Builder':
        return self

    def step_limit(self, step_limit: int) -> 'Builder':
        return self

    def timestamp(self, timestamp_us: int) -> 'Builder':
        return self

    def nid(self, nid: int) -> 'Builder':
        return self

    def signature(self, signature: bytes) -> 'Builder':
        return self

    def data_type(self, data_type: str) -> 'Builder':
        return self

    def data(self, params: Union[dict, str]) -> 'Builder':
        return self

    def build(self) -> 'RpcRequest':
        request = self._request
        self._request = None
        return request
