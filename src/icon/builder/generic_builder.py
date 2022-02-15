# -*- coding: utf-8 -*-

from __future__ import annotations

import copy
from typing import Dict, Any

from ..utils import to_str_dict


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
