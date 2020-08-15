# -*- coding: utf-8 -*-
# Copyright 2020 ICON Foundation
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

from typing import Dict, Any, Union

from . import builder
from .builder.method import Method
from .data.address import Address
from .data.block import Block
from .data.exception import JSONRPCException, ArgumentException
from .data.rpc_request import RpcRequest
from .data.rpc_response import RpcResponse
from .data.transaction import Transaction
from .data.transaction_result import TransactionResult
from .provider.provider import Provider
from .utils.type import str_to_int, bytes_to_hex, hex_to_bytes


class Client(object):
    def __init__(self, provider: Provider, defaults: Dict[str, Any] = None):
        if defaults is None:
            defaults = {}
        elif not isinstance(defaults, dict):
            raise ValueError(f"Invalid params: defaults={defaults}")

        self._provider = provider
        self._defaults = defaults

    @property
    def defaults(self) -> Dict[str, Any]:
        return self._defaults

    def get_block_by_hash(self, block_hash: bytes) -> Block:
        params = {"hash": bytes_to_hex(block_hash)}
        response = self._send(Method.GET_BLOCK_BY_HASH, params)
        return Block.from_dict(response.result)

    def get_block_by_height(self, block_height: int) -> Block:
        if not (isinstance(block_height, int) and block_height >= 0):
            raise ValueError(f"Invalid params: {block_height}")

        params = {"height": hex(block_height)}
        response = self._send(Method.GET_BLOCK_BY_HEIGHT, params)
        return Block.from_dict(response.result)

    def get_last_block(self) -> Block:
        response = self._send(Method.GET_LAST_BLOCK)
        return Block.from_dict(response.result)

    def get_transaction(self, tx_hash: bytes) -> Transaction:
        params = {"txHash": bytes_to_hex(tx_hash)}
        response = self._send(Method.GET_TRANSACTION_BY_HASH, params)
        return Transaction.from_dict(response.result)

    def get_transaction_result(self, tx_hash: bytes) -> TransactionResult:
        params = {"txHash": bytes_to_hex(tx_hash)}
        response = self._send(Method.GET_TRANSACTION_RESULT, params)
        return TransactionResult.from_dict(response.result)

    def get_total_supply(self) -> int:
        response = self._send(Method.GET_TOTAL_SUPPLY)
        return str_to_int(response.result)

    def get_balance(self, address: Address) -> int:
        params = {"address": str(address)}
        response = self._send(Method.GET_BALANCE, params)
        return str_to_int(response.result)

    def get_score_api(self, address: Address) -> Dict[str, str]:
        params = {"address": str(address)}
        response = self._send(Method.GET_SCORE_API, params)
        return response.result

    def get_block(self, value: Union[bytes, int, None] = None) -> Dict[str, str]:
        if isinstance(value, bytes):
            params = {"hash": bytes_to_hex(value)}
        elif isinstance(value, int):
            params = {"hash": hex(value)}
        elif value is None:
            params = None
        else:
            raise ArgumentException(f"Invalid argument: {value}")

        response = self._send(Method.GET_BLOCK, params)
        return response.result

    def send_transaction(
        self, tx: Transaction, estimate: bool = False
    ) -> Union[int, bytes]:
        if not isinstance(tx, Transaction):
            ValueError(f"Invalid params: tx={tx}")

        if estimate:
            ret: int = self.estimate_step(tx)
        else:
            ret: bytes = self._send_transaction(tx)

        return ret

    def _send_transaction(self, tx: Transaction) -> bytes:
        response = self._send(Method.SEND_TRANSACTION, tx)
        return hex_to_bytes(response.result)

    def call(self, params: Dict[str, str]) -> Union[str, Dict[str, str]]:
        response = self._send(Method.CALL, params)
        return response.result

    def estimate_step(self, tx: builder.Transaction) -> int:
        response = self._send(Method.ESTIMATE_STEP, tx)
        return str_to_int(response.result)

    def get_status(self) -> Dict[str, str]:
        params = {"filter": ["lastBlock"]}
        response = self._send(Method.GET_STATUS, params)
        return response.result

    def _send(
        self, method: str, params: Union[Transaction, Dict[str, str]] = None
    ) -> RpcResponse:
        request = RpcRequest(method, params)
        response = self._provider.send(request)

        if response.error:
            raise JSONRPCException(f"{response.error}")

        return response

    def send(self, request: RpcRequest) -> RpcResponse:
        return self._provider.send(request)
