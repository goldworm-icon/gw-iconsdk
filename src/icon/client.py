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

if TYPE_CHECKING:
    from .data.block import Block
    from .data.transaction import Transaction
    from .data.transaction_result import TransactionResult
    from .provider.provider import Provider


class Client(object):
    def __init__(self, provider: Provider):
        self._provider = provider

    def get_block(self) -> Block:
        pass

    def get_transaction(self) -> Transaction:
        pass

    def get_transaction_result(self) -> TransactionResult:
        pass

    def get_total_supply(self) -> int:
        pass

    def get_balance(self) -> int:
        pass

    def get_score_api(self) -> Dict[str, str]:
        pass

    def send_transaction(self):
        pass

    def call(self):
        pass

    def estimate_step(self) -> int:
        pass
