# -*- coding: utf-8 -*-

from __future__ import annotations

import base64
import json
from enum import IntEnum, auto
from typing import Optional, Dict, Union, Any

from .address import Address
from .utils import str_to_int, hex_to_bytes, bytes_to_hex
from ..builder.key import Key
from ..exception import JSONRPCException


class DataType(IntEnum):
    BASE = auto()
    CALL = auto()
    DEPLOY = auto()
    MESSAGE = auto()
    NONE = auto()

    def __str__(self) -> str:
        return self.name.lower()


def get_transaction(data: Dict[str, Any]) -> Union[Transaction, BaseTransaction]:
    data_type: str = data.get(Key.DATA_TYPE, "")
    if data_type == "base":
        return BaseTransaction.from_dict(data)
    else:
        return Transaction.from_dict(data)


class _JSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Address):
            return str(o)
        elif isinstance(o, bytes):
            return bytes_to_hex(o)

        return json.JSONEncoder.default(self, o)


def _default(o: Any) -> Any:
    if isinstance(o, Address):
        return str(o)
    elif isinstance(o, bytes):
        return bytes_to_hex(o)

    return o


class Transaction(object):
    """Transaction class containing transaction information from
    """

    def __init__(
        self,
        version: int,
        nid: int,
        from_: Optional[Address],
        to: Optional[Address],
        step_limit: int,
        timestamp: int,
        signature: bytes,
        block_height: int = None,
        block_hash: bytes = None,
        tx_hash: bytes = None,
        tx_index: int = None,
        value: int = 0,
        nonce: Optional[int] = None,
        data_type: Optional[str] = None,
        data: Optional[Union[str, Dict[str, Any]]] = None,
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

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4, default=_default)

    @property
    def version(self) -> int:
        return self._version

    @property
    def nid(self) -> int:
        return self._nid

    @property
    def from_(self) -> Address:
        """
        The account who created the transaction.
        """
        return self._from

    @property
    def to(self) -> Address:
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
    def from_bytes(cls, data: bytes) -> Transaction:
        data = json.loads(data)
        return cls.from_dict(data)

    def to_dict(self) -> Dict[str, Any]:
        ret = {
            "version": self._version,
            "nid": self._nid,
            "from": self._from,
            "to": self._to,
            "value": self._value,
            "stepLimit": self._step_limit,
            "timestamp": self._timestamp,
            "signature": bytes_to_hex(self._signature),
        }

        keys = (
            "nonce", "dataType", "data",
            "txIndex", "txHash", "blockHeight", "blockHash"
        )
        values = (
            self._nonce, self._data_type, self._data,
            self._tx_index, self._tx_hash, self._block_height, self._block_hash
        )
        for key, value in zip(keys, values):
            if value is not None:
                ret[key] = value

        return ret

    @classmethod
    def from_dict(cls, tx_dict: Dict[str, str]) -> Transaction:
        version = str_to_int(tx_dict["version"])
        nid = str_to_int(tx_dict.get("nid", "0x0"))
        from_ = Address.from_string(tx_dict["from"])
        to = Address.from_string(tx_dict["to"])
        value = str_to_int(tx_dict.get("value", "0x0"))
        tx_index = str_to_int(tx_dict["txIndex"]) if "txIndex" in tx_dict else None
        tx_hash = hex_to_bytes(tx_dict["txHash"]) if "txHash" in tx_dict else None
        block_height = str_to_int(tx_dict["blockHeight"]) if "blockHeight" in tx_dict else None
        block_hash = hex_to_bytes(tx_dict["blockHash"]) if "blockHash" in tx_dict else None
        step_limit = str_to_int(tx_dict["stepLimit"])
        timestamp = cls._get_timestamp(tx_dict)
        signature: bytes = base64.b64decode(tx_dict["signature"])
        data_type = tx_dict.get("dataType")
        nonce: int = cls._get_nonce(tx_dict.get("nonce"))
        data: Any = cls._get_data(tx_dict)

        return cls(
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


class BaseTransaction(object):

    class PRep(object):
        def __init__(self, irep: int, rrep: int, total_delegation: int, value: int):
            self._irep = irep
            self._rrep = rrep
            self._total_delegation = total_delegation
            self._value = value

        def __repr__(self):
            return str(self.to_dict())

        @property
        def irep(self) -> int:
            return self._irep

        @property
        def rrep(self) -> int:
            return self._rrep

        @property
        def total_delegation(self) -> int:
            return self._total_delegation

        @property
        def value(self) -> int:
            return self._value

        def to_dict(self) -> Dict[str, Any]:
            return {
                "irep": self._irep,
                "rrep": self._rrep,
                "totalDelegation": self._total_delegation,
                "value": self._value
            }

        @classmethod
        def from_dict(cls, data: Dict[str, Any]) -> BaseTransaction.PRep:
            return cls(
                irep=str_to_int(data["irep"]),
                rrep=str_to_int(data["rrep"]),
                total_delegation=str_to_int(data["totalDelegation"]),
                value=str_to_int(data["value"])
            )

    class Result(object):
        def __init__(self, covered_by_fee: int, covered_by_over_issued_icx: int, issue: int):
            self._covered_by_fee = covered_by_fee
            self._covered_by_over_issued_icx = covered_by_over_issued_icx
            self._issue = issue

        def __repr__(self) -> str:
            return str(self.to_dict())

        @property
        def covered_by_fee(self) -> int:
            return self._covered_by_fee

        @property
        def covered_by_over_issued_icx(self) -> int:
            return self._covered_by_over_issued_icx

        @property
        def issue(self) -> int:
            return self._issue

        def to_dict(self) -> Dict[str, Any]:
            return {
                "coveredByFee": self._covered_by_fee,
                "coveredByOverIssuedICX": self._covered_by_over_issued_icx,
                "issue": self._issue
            }

        @classmethod
        def from_dict(cls, data: Dict[str, Any]) -> BaseTransaction.Result:
            return cls(
                covered_by_fee=str_to_int(data["coveredByFee"]),
                covered_by_over_issued_icx=str_to_int(data["coveredByOverIssuedICX"]),
                issue=str_to_int(data["issue"])
            )

    def __init__(self, version: int, timestamp: int, data_type: str, data: Dict[str, Any]):
        self._version = version
        self._timestamp = timestamp
        self._data_type = data_type
        self._data = data

    def __repr__(self) -> str:
        data: Dict[str, Any] = self.to_dict()
        return json.dumps(data, indent=4)

    @property
    def version(self) -> version:
        return self._version

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def data_type(self) -> str:
        return self._data_type

    @property
    def data(self) -> Dict[str, Any]:
        return self._data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self._version,
            "timestamp": self._timestamp,
            "dataType": self._data_type,
            "data": {
                "prep": self._data["prep"].to_dict(),
                "result": self._data["result"].to_dict(),
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BaseTransaction:
        return cls(
            version=str_to_int(data["version"]),
            timestamp=str_to_int(data["timestamp"]),
            data_type=data["dataType"],
            data={
                "prep": BaseTransaction.PRep.from_dict(data["data"]["prep"]),
                "result": BaseTransaction.Result.from_dict(data["data"]["result"])
            }
        )
