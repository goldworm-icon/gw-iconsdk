# -*- coding: utf-8 -*-
# Copyright 2020 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import TYPE_CHECKING, Union, Dict

from ..data.rpc_request import RpcRequest

if TYPE_CHECKING:
    from ..data.address import Address


class GenericBuilder(object):
    def __init__(self, method: str, params: Dict = None):
        self._request = RpcRequest(method, params)

    def add(self, key: str, value: Union[bool, int, bytes, str, "Address"]):
        self._request.params[key] = value
        return self

    def set_data(self, data: Union[bytes, str, Dict[str, Union[bool, int, bytes, str, "Address"]]]):
        self._request.params["data"] = data
        return self

    def build(self) -> "RpcRequest":
        request = self._request
        self._request = None
        return request
