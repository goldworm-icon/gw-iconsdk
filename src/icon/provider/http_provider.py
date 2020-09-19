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

import requests

from .provider import Provider
from ..builder.method import Method
from ..data.rpc_request import RpcRequest
from ..data.rpc_response import RpcResponse


class HTTPProvider(Provider):
    def __init__(self, base_url: str, version: int = 3):
        """

        :param base_url: ex) https://localhost:9000
        """

        self._base_url = base_url
        self._version = version
        self._hooks = {}

        self._url = "/".join((self._base_url, "api", f"v{version}"))
        self._debug_url = "/".join((self._base_url, "api", "debug", f"v{version}"))

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def version(self) -> int:
        return self._version

    def send(self, request: RpcRequest, **kwargs) -> RpcResponse:
        url = self._get_url(request.method)
        request.url = url

        response: requests.Response = requests.post(url, json=request.to_dict())

        if "hooks" in kwargs:
            self._dispatch_hook("response", kwargs["hooks"], response)

        rpc_response = RpcResponse(response.json())
        rpc_response.user_data = response
        return rpc_response

    def _get_url(self, method: str) -> str:
        if method in {Method.ESTIMATE_STEP, Method.GET_ACCOUNT}:
            return self._debug_url

        return self._url

    @staticmethod
    def _dispatch_hook(key: str, hooks, hook_data: requests.Response):
        hooks = hooks or {}
        hooks = hooks.get(key)
        if not hooks:
            return

        if hasattr(hooks, "__call__"):
            hooks = [hooks]

        for hook in hooks:
            _hook_data = hook(hook_data)
            if _hook_data is not None:
                hook_data = _hook_data
