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

from __future__ import annotations

import copy
from typing import Dict, Any

from ..data.utils import to_str_dict


class GenericBuilder(object):
    def __init__(self, params: Dict[str, Any] = None):
        self._params = params if isinstance(params, dict) else {}

    def add(self, key: str, value: Any) -> GenericBuilder:
        self._params[key] = value
        return self

    def remove(self, key: str) -> GenericBuilder:
        if key in self._params:
            del self._params[key]

        return self

    def update(self, params: Dict[str, Any]) -> GenericBuilder:
        for k, v in params.items():
            self.add(k, copy.deepcopy(v))

        return self

    def build(self) -> Dict[str, str]:
        return to_str_dict(self._params)
