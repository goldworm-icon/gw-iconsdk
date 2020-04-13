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

from typing import TYPE_CHECKING, Dict

from .builder.generic_builder import GenericBuilder
from .builder.method import Method
from .data.address import Address
from .data.transaction import Transaction
from .data.transaction_result import TransactionResult
from .utils.convert_type import str_to_int

if TYPE_CHECKING:
    from .data.block import Block
    from .data.transaction import Transaction
    from .provider.provider import Provider


class Client(object):
    def __init__(self, provider: "Provider"):
        self._provider = provider

    def get_block(self) -> "Block":
        pass

    def get_transaction(self, tx_hash: bytes) -> "Transaction":
        builder = GenericBuilder(Method.GET_TRANSACTION_BY_HASH)
        builder.add("txHash", tx_hash)
        request = builder.build()

        response = self._provider.send(request)
        return Transaction.from_dict(response.result)

    def get_transaction_result(self, tx_hash: bytes) -> "TransactionResult":
        builder = GenericBuilder(Method.GET_TRANSACTION_RESULT)
        builder.add("txHash", tx_hash)
        request = builder.build()

        response = self._provider.send(request)
        return TransactionResult.from_dict(response.result)

    def get_total_supply(self) -> int:
        builder = GenericBuilder(Method.GET_TOTAL_SUPPLY)
        request = builder.build()

        response = self._provider.send(request)
        return str_to_int(response.result)

    def get_balance(self, address: Address) -> int:
        builder = GenericBuilder(Method.GET_BALANCE, {"address": address})
        request = builder.build()

        response = self._provider.send(request)
        return str_to_int(response.result)

    def get_score_api(self) -> Dict[str, str]:
        pass

    def send_transaction(self):
        pass

    def call(self):
        pass

    def estimate_step(self) -> int:
        pass
