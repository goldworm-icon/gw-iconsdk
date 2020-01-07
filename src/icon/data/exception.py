# -*- coding: utf-8 -*-
# Copyright 2018 ICON Foundation
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

from enum import IntEnum, unique
from typing import Optional


@unique
class IconServiceExceptionCode(IntEnum):
    """Result code enumeration"""
    OK = 0
    KEY_STORE_ERROR = 1
    ADDRESS_ERROR = 2
    BALANCE_ERROR = 3
    DATA_TYPE_ERROR = 4
    JSON_RPC_ERROR = 5
    ZIP_MEMORY_ERROR = 6
    URL_ERROR = 7

    def __str__(self) -> str:
        return str(self.name).capitalize().replace('_', ' ')


class SDKException(BaseException):

    def __init__(self, code: IconServiceExceptionCode, message: Optional[str]):
        self._code = code
        self._message = message if isinstance(message, str) else str(code)

    @property
    def message(self):
        return self._message

    @property
    def code(self):
        return self._code

    def __str__(self):
        return f"{self.message} ({self._code.value})"


class KeyStoreException(SDKException):
    """"Error when making or loading a keystore file."""

    def __init__(self, message: Optional[str]):
        super().__init__(IconServiceExceptionCode.KEY_STORE_ERROR, message)


class AddressException(SDKException):
    """Error when having an invalid address."""

    def __init__(self, message: Optional[str]):
        super().__init__(IconServiceExceptionCode.ADDRESS_ERROR, message)


class BalanceException(SDKException):
    """Error when having an invalid balance."""

    def __init__(self, message: Optional[str]):
        super().__init__(IconServiceExceptionCode.BALANCE_ERROR, message)


class DataTypeException(SDKException):
    """Error when data type is invalid."""

    def __init__(self, message: Optional[str]):
        super().__init__(IconServiceExceptionCode.DATA_TYPE_ERROR, message)


class JSONRPCException(SDKException):
    """Error when get JSON-RPC Error Response."""

    def __init__(self, message: Optional[str]):
        super().__init__(IconServiceExceptionCode.JSON_RPC_ERROR, message)


class ZipException(SDKException):
    """"Error while write zip in memory"""

    def __init__(self, message: Optional[str]):
        super().__init__(IconServiceExceptionCode.ZIP_MEMORY_ERROR, message)


class URLException(SDKException):
    """Error regarding invalid URL"""

    def __init__(self, message: Optional[str]):
        super().__init__(IconServiceExceptionCode.URL_ERROR, message)
