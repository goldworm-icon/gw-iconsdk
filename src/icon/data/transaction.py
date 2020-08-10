# -*- coding: utf-8 -*-

import base64
import json
from enum import IntEnum, auto
from typing import Optional, Dict, Union, Any

from .address import Address
from .exception import JSONRPCException
from ..utils.convert_type import str_to_int, hex_to_bytes, bytes_to_hex


class DataType(IntEnum):
    NONE = auto()
    CALL = auto()
    DEPLOY = auto()
    MESSAGE = auto()

    def __str__(self) -> str:
        return self.name.lower()


class Transaction(object):
    """Transaction class containing transaction information from
    """

    def __init__(
        self,
        version: int,
        nid: int,
        from_: Optional["Address"],
        to: Optional["Address"],
        step_limit: int,
        timestamp: int,
        signature: bytes,
        block_height: int,
        block_hash: bytes,
        tx_hash: bytes,
        tx_index: int,
        value: int = 0,
        nonce: Optional[int] = None,
        data_type: Optional[str] = None,
        data: Optional[Union[str, Dict]] = None,
    ) -> None:
        """Transaction class for icon score context
        """
        self._version = version
        self._nid = nid
        self._tx_hash = tx_hash
        self._tx_index = tx_index
        self._from = from_
        self._to = to
        self._step_limit = step_limit
        self._value = value
        self._timestamp = timestamp
        self._signature = signature
        self._block_height = block_height
        self._block_hash = block_hash
        self._nonce = nonce
        self._data_type = data_type
        self._data = data

    def __str__(self):
        items = (
            f"version={self._version}",
            f"nid={self._nid}",
            f"block_hash={bytes_to_hex(self._block_hash)}",
            f"block_height={self._block_height}",
            f"tx_hash={bytes_to_hex(self._tx_hash)}",
            f"tx_index={self._tx_index}",
            f"from={self._from}",
            f"to={self._to}",
            f"value={self._value}",
            f"step_limit={self._step_limit}",
            f"timestamp={self._timestamp}",
            f"signature={bytes_to_hex(self._signature)}",
            f"data_type={self._data_type}",
            f"data={self._data}",
        )

        return "\n".join(items)

    @property
    def version(self) -> int:
        return self._version

    @property
    def nid(self) -> int:
        return self._nid

    @property
    def from_(self) -> "Address":
        """
        The account who created the transaction.
        """
        return self._from

    @property
    def to(self) -> "Address":
        """
        The account of tx to.
        """
        return self._to

    @property
    def tx_index(self) -> int:
        """
        Transaction index in a block
        """
        return self._tx_index

    @property
    def tx_hash(self) -> bytes:
        """
        Transaction hash
        """
        return self._tx_hash

    @property
    def block_height(self) -> int:
        return self._block_height

    @property
    def block_hash(self) -> bytes:
        return self._block_hash

    @property
    def timestamp(self) -> int:
        """
        Timestamp of a transaction request in microseconds
        This is NOT a block timestamp
        """
        return self._timestamp

    @property
    def nonce(self) -> Optional[int]:
        """
        (optional)
        nonce of a transaction request.
        random value
        """
        return self._nonce

    @property
    def value(self) -> int:
        return self._value

    @property
    def data_type(self) -> Optional[str]:
        return self._data_type

    @property
    def data(self) -> Optional[Any]:
        return self._data

    @property
    def signature(self) -> bytes:
        return self._signature

    @classmethod
    def from_bytes(cls, data: bytes) -> "Transaction":
        data = json.loads(data)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, tx_dict: Dict[str, str]) -> "Transaction":
        version = str_to_int(tx_dict["version"])
        nid = str_to_int(tx_dict["nid"])
        from_ = Address.from_string(tx_dict["from"])
        to = Address.from_string(tx_dict["to"])
        value = str_to_int(tx_dict.get("value", "0x0"))
        tx_index = str_to_int(tx_dict["txIndex"])
        tx_hash = hex_to_bytes(tx_dict["txHash"])
        block_height = str_to_int(tx_dict["blockHeight"])
        block_hash = hex_to_bytes(tx_dict["blockHash"])
        step_limit = str_to_int(tx_dict["stepLimit"])
        timestamp = cls._get_timestamp(tx_dict)
        signature: bytes = base64.b64decode(tx_dict["signature"])
        data_type = tx_dict.get("dataType")
        nonce: int = cls._get_nonce(tx_dict.get("nonce"))
        data: Any = cls._get_data(tx_dict)

        return Transaction(
            version=version,
            nid=nid,
            nonce=nonce,
            from_=from_,
            to=to,
            value=value,
            tx_index=tx_index,
            tx_hash=tx_hash,
            signature=signature,
            block_height=block_height,
            block_hash=block_hash,
            step_limit=step_limit,
            timestamp=timestamp,
            data_type=data_type,
            data=data,
        )

    @staticmethod
    def _get_nonce(value: Optional[str]) -> Optional[int]:
        return str_to_int(value) if value else None

    @staticmethod
    def _get_timestamp(tx_dict: Dict[str, str]) -> int:
        for key in ("timestamp", "time_stamp"):
            if key in tx_dict:
                return str_to_int(tx_dict[key])

        raise JSONRPCException("No timestamp in transaction")

    @staticmethod
    def _get_data(tx_dict: Dict[str, str]) -> Any:
        return tx_dict.get("data")
