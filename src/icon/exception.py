# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Optional, Any


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
        BUILDER_ERROR = 8
        ARG_ERROR = 9
        HOOK_ERROR = 10

        def __str__(self) -> str:
            return str(self.name).capitalize().replace("_", " ")

    def __init__(self, code: Code, message: Optional[str], user_data: Any = None):
        self._code = code
        self._message = message if isinstance(message, str) else str(code)
        self._user_data = user_data

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message

    @property
    def user_data(self) -> Any:
        return self._user_data

    def __str__(self):
        return f"{self.message} ({self._code.value})"


class KeyStoreException(SDKException):
    """"Error when making or loading a keystore file."""

    def __init__(self, message: Optional[str], user_data: Any = None):
        super().__init__(SDKException.Code.KEY_STORE_ERROR, message, user_data)


class AddressException(SDKException):
    """Error when having an invalid address."""

    def __init__(self, message: Optional[str], user_data: Any = None):
        super().__init__(SDKException.Code.ADDRESS_ERROR, message, user_data)


class BalanceException(SDKException):
    """Error when having an invalid balance."""

    def __init__(self, message: Optional[str], user_data: Any = None):
        super().__init__(SDKException.Code.BALANCE_ERROR, message, user_data)


class DataTypeException(SDKException):
    """Error when data type is invalid."""

    def __init__(self, message: Optional[str], user_data: Any = None):
        super().__init__(SDKException.Code.DATA_TYPE_ERROR, message, user_data)


class ArgumentException(SDKException):
    def __init__(self, message: Optional[str], user_data: Any = None):
        super().__init__(SDKException.Code.ARG_ERROR, message, user_data)


class JSONRPCException(SDKException):
    """Error when get JSON-RPC Error Response."""

    def __init__(self, message: Optional[str], user_data: Any = None):
        super().__init__(SDKException.Code.JSON_RPC_ERROR, message, user_data)


class ZipException(SDKException):
    """"Error while write zip in memory"""

    def __init__(self, message: Optional[str], user_data: Any = None):
        super().__init__(SDKException.Code.ZIP_MEMORY_ERROR, message, user_data)


class URLException(SDKException):
    """Error regarding invalid URL"""

    def __init__(self, message: Optional[str], user_data: Any = None):
        super().__init__(SDKException.Code.URL_ERROR, message, user_data)


class BuilderException(SDKException):
    """Error for sdk method misuse
    """

    def __init__(self, message: Optional[str], user_data: Any = None):
        super().__init__(SDKException.Code.BUILDER_ERROR, message, user_data)


class HookException(SDKException):
    def __init__(self, message: Optional[str], user_data: Any = None):
        super().__init__(SDKException.Code.HOOK_ERROR, message, user_data)
