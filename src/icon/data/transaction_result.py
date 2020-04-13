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

from enum import IntEnum
from typing import List, Dict, Optional

from .address import Address
from .event_log import EventLog
from ..utils.convert_type import hex_to_bytes, str_to_int


class TransactionResult(object):
    """Represents the result of a transaction

    """

    class Status(IntEnum):
        FAILURE = 0
        SUCCESS = 1

    class Failure(object):
        def __init__(self, code: int, message: str):
            self._code = code
            self._message = message

        @property
        def code(self) -> int:
            return self._code

        @property
        def message(self) -> str:
            return self._message

        @classmethod
        def from_dict(cls, data: Dict[str, str]) -> "TransactionResult.Failure":
            code = str_to_int(data["code"])
            message = data["message"]

            return cls(code, message)

    def __init__(
        self,
        tx_hash: bytes = None,
        status: Status = Status.FAILURE,
        failure: Failure = None,
        tx_index: int = -1,
        to: "Address" = None,
        block_height: int = -1,
        block_hash: bytes = None,
        cumulative_step_used: int = -1,
        step_price: int = -1,
        step_used: int = -1,
        score_address: "Address" = None,
        logs_bloom: bytes = None,
        event_logs: List["EventLog"] = None,
    ):
        self._status: Optional["TransactionResult.Status"] = status
        self._failure: Optional["TransactionResult.Failure"] = failure
        self._tx_hash: bytes = tx_hash
        self._tx_index: int = tx_index
        self._to: "Address" = to
        self._block_height: int = block_height
        self._block_hash: bytes = block_hash
        self._cumulative_step_used: int = cumulative_step_used
        self._step_price = step_price
        self._step_used = step_used
        self._score_address: Optional["Address"] = score_address
        self._fee = step_price * step_used
        self._logs_bloom: Optional[bytes] = logs_bloom
        self._event_logs: List["EventLog"] = [] if event_logs is None else event_logs

    @property
    def status(self) -> Status:
        return self._status

    @property
    def failure(self) -> Optional["TransactionResult.Failure"]:
        return self._failure

    @property
    def tx_hash(self) -> bytes:
        return self._tx_hash

    @property
    def tx_index(self) -> int:
        return self._tx_index

    @property
    def to(self) -> "Address":
        return self._to

    @property
    def block_height(self) -> int:
        return self._block_height

    @property
    def block_hash(self) -> bytes:
        return self._block_hash

    @property
    def step_price(self) -> int:
        return self._step_price

    @property
    def step_used(self) -> int:
        return self._step_used

    @property
    def cumulative_step_used(self) -> int:
        return self._cumulative_step_used

    @property
    def score_address(self) -> "Address":
        return self._score_address

    @property
    def fee(self) -> int:
        return self._fee

    @property
    def logs_bloom(self) -> Optional[bytes]:
        return self._logs_bloom

    @property
    def event_logs(self) -> List["EventLog"]:
        return self._event_logs

    @classmethod
    def from_dict(cls, data: dict) -> "TransactionResult":
        status = TransactionResult.Status(str_to_int(data["status"]))
        failure = (
            TransactionResult.Failure.from_dict(data["failure"])
            if "failure" in data
            else None
        )
        tx_hash: bytes = hex_to_bytes(data["txHash"])
        tx_index: int = str_to_int(data["txIndex"])
        to: "Address" = Address.from_string(data["to"])
        block_height: int = str_to_int(data["blockHeight"])
        block_hash: bytes = hex_to_bytes(data["blockHash"])
        step_price: int = str_to_int(data["stepPrice"])
        step_used: int = str_to_int(data["stepUsed"])
        cumulative_step_used = str_to_int(data["cumulativeStepUsed"])
        score_address = (
            Address.from_string(data["scoreAddress"])
            if "scoreAddress" in data
            else None
        )
        logs_bloom: bytes = hex_to_bytes(data.get("logsBloom"))
        event_logs: List["EventLog"] = cls._parse_event_logs(data["eventLogs"])

        return TransactionResult(
            status=status,
            failure=failure,
            to=to,
            tx_hash=tx_hash,
            tx_index=tx_index,
            block_height=block_height,
            block_hash=block_hash,
            step_price=step_price,
            step_used=step_used,
            cumulative_step_used=cumulative_step_used,
            score_address=score_address,
            logs_bloom=logs_bloom,
            event_logs=event_logs,
        )

    @classmethod
    def _parse_event_logs(cls, event_logs: List[Dict[str, str]]) -> List["EventLog"]:
        ret = []
        for log in event_logs:
            ret.append(EventLog.from_dict(log))

        return ret
