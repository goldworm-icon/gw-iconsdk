# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, Union, Dict

from ..data.rpc_request import RpcRequest

if TYPE_CHECKING:
    from ..data.address import Address


class GenericBuilder(object):
    def __init__(self, method: str):
        self._request = RpcRequest(method)

    def add(self, key: str, value: Union[bool, int, bytes, str, Address]):
        self._request.params[key] = value
        return self

    def set_data(self, data: Union[bytes, str, Dict[str, Union[bool, int, bytes, str, Address]]]):
        self._request.params["data"] = data
        return self

    def build(self) -> 'RpcRequest':
        request = self._request
        self._request = None
        return request
