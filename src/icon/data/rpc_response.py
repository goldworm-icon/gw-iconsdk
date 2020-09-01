# -*- coding: utf-8 -*-

import json
from typing import Dict, Optional, Union, Any


class RpcResponse(object):
    def __init__(self, json_text: Dict[str, Any]):
        self._json = json_text
        self._user_data = None

    def __str__(self):
        return json.dumps(self._json, indent=4)

    @property
    def error(self) -> Optional[Dict[str, Union[int, str]]]:
        return self._json.get("error")

    @property
    def result(self) -> Optional[Union[str, Dict[str, str]]]:
        return self._json.get("result")

    @property
    def user_data(self) -> Any:
        return self._user_data

    @user_data.setter
    def user_data(self, value: Any):
        self._user_data = value
