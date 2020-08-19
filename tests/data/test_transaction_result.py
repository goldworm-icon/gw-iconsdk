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

from icon.data import bytes_to_hex
from icon.data.transaction_result import TransactionResult


class TestTransactionResult(object):
    def test_from_dict_with_icx_transfer_tx(
        self, block_hash, tx_hash, address, step_price, logs_bloom
    ):
        block_height = 0xE65585
        tx_index = 0x2
        step_used = 0x186A0
        cumulative_step_used = 0x12345678
        status = TransactionResult.Status.SUCCESS

        data_in_dict = {
            "txHash": bytes_to_hex(tx_hash),
            "blockHeight": hex(block_height),
            "blockHash": bytes_to_hex(block_hash),
            "txIndex": hex(tx_index),
            "to": str(address),
            "stepUsed": hex(step_used),
            "stepPrice": hex(step_price),
            "cumulativeStepUsed": hex(cumulative_step_used),
            "eventLogs": [],
            "logsBloom": bytes_to_hex(logs_bloom),
            "status": hex(status),
        }

        tx_result = TransactionResult.from_dict(data_in_dict)
        assert tx_result.status == status
        assert tx_result.failure is None
        assert tx_result.tx_hash == tx_hash
        assert tx_result.block_height == block_height
        assert tx_result.block_hash == block_hash
        assert tx_result.tx_index == tx_index
        assert tx_result.to == address
        assert tx_result.step_used == step_used
        assert tx_result.step_price == step_price
        assert tx_result.cumulative_step_used == cumulative_step_used
        assert tx_result.fee == step_price * step_used
        assert tx_result.score_address is None
        assert len(tx_result.event_logs) == 0
