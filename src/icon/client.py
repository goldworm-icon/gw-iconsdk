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

from typing import Dict

from .builder.generic_builder import GenericBuilder
from .builder.method import Method
from .data.address import Address
from .data.block import Block
from .data.rpc_request import RpcRequest
from .data.transaction import Transaction
from .data.transaction_result import TransactionResult
from .provider.provider import Provider
from .utils.convert_type import str_to_int, bytes_to_hex


class Client(object):
    def __init__(self, provider: Provider):
        self._provider = provider

    def get_block_by_hash(self, block_hash: bytes) -> Block:
        params = {"txHash": bytes_to_hex(block_hash)}
        request = RpcRequest(Method.GET_BLOCK_BY_HASH, params)
        response = self._provider.send(request)
        return Block.from_dict(response.result)

    def get_block_by_height(self, block_height: int) -> Block:
        if not (isinstance(block_height, int) and block_height >= 0):
            raise ValueError(f"Invalid params: {block_height}")

        params = {"txHash": hex(block_height)}
        request = RpcRequest(Method.GET_BLOCK_BY_HASH, params)
        response = self._provider.send(request)
        return Block.from_dict(response.result)

    def get_transaction(self, tx_hash: bytes) -> Transaction:
        params = {"txHash": bytes_to_hex(tx_hash)}
        request = RpcRequest(Method.GET_TRANSACTION_BY_HASH, params)
        response = self._provider.send(request)
        return Transaction.from_dict(response.result)

    def get_transaction_result(self, tx_hash: bytes) -> TransactionResult:
        builder = GenericBuilder(Method.GET_TRANSACTION_RESULT)
        builder.add("txHash", tx_hash)
        params: Dict[str, str] = builder.build()

        request = RpcRequest(Method.GET_TRANSACTION_RESULT, params)
        response = self._provider.send(request)
        return TransactionResult.from_dict(response.result)

    def get_total_supply(self) -> int:
        request = RpcRequest(Method.GET_TOTAL_SUPPLY)
        response = self._provider.send(request)
        return str_to_int(response.result)

    def get_balance(self, address: Address) -> int:
        request = RpcRequest(Method.GET_BALANCE, {"address": str(address)})
        response = self._provider.send(request)
        return str_to_int(response.result)

    def get_score_api(self, address: Address) -> Dict[str, str]:
        request = RpcRequest(Method.GET_SCORE_API, {"address": str(address)})
        response = self._provider.send(request)
        return response.result

    def send_transaction(self, params: Dict[str, str] = None):
        request = RpcRequest(Method.SEND_TRANSACTION, params)
        response = self._provider.send(request)
        return response

    def call(self, params: Dict[str, str]):
        request = RpcRequest(Method.CALL, params)
        response = self._provider.send(request)
        return response.result

    def estimate_step(self, params: Dict[str, str]) -> int:
        request = RpcRequest(Method.ESTIMATE_STEP, params)
        response = self._provider.send(request)
        return str_to_int(response.result)
