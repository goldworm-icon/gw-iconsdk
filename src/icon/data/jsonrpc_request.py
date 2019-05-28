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

from .dict import Dict
from typing import Optional


class JsonRpcRequest(object):
    def __init__(self, method: str, params: Dict = None, _id: int = 0):
        self._version = "2.0"
        self._method = method
        self._params = params
        self._id = _id

    @property
    def params(self) -> Optional[Dict]:
        return self._params

    @property
    def method(self) -> Optional[str]:
        return self._method

    def __str__(self) -> str:
        pass
