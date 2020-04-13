# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Optional


class SDKException(Exception):
    @unique
    class Code(IntEnum):
        OK = 0
        KEY_STORE_ERROR = 1
        ADDRESS_ERROR = 2
        BALANCE_ERROR = 3
        DATA_TYPE_ERROR = 4
        JSON_RPC_ERROR = 5
        ZIP_MEMORY_ERROR = 6
        URL_ERROR = 7

        def __str__(self) -> str:
            return str(self.name).capitalize().replace("_", " ")

    def __init__(self, code: Code, message: Optional[str]):
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
        super().__init__(SDKException.Code.KEY_STORE_ERROR, message)


class AddressException(SDKException):
    """Error when having an invalid address."""

    def __init__(self, message: Optional[str]):
        super().__init__(SDKException.Code.ADDRESS_ERROR, message)


class BalanceException(SDKException):
    """Error when having an invalid balance."""

    def __init__(self, message: Optional[str]):
        super().__init__(SDKException.Code.BALANCE_ERROR, message)


class DataTypeException(SDKException):
    """Error when data type is invalid."""

    def __init__(self, message: Optional[str]):
        super().__init__(SDKException.Code.DATA_TYPE_ERROR, message)


class JSONRPCException(SDKException):
    """Error when get JSON-RPC Error Response."""

    def __init__(self, message: Optional[str]):
        super().__init__(SDKException.Code.JSON_RPC_ERROR, message)


class ZipException(SDKException):
    """"Error while write zip in memory"""

    def __init__(self, message: Optional[str]):
        super().__init__(SDKException.Code.ZIP_MEMORY_ERROR, message)


class URLException(SDKException):
    """Error regarding invalid URL"""

    def __init__(self, message: Optional[str]):
        super().__init__(SDKException.Code.URL_ERROR, message)
