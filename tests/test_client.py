# -*- coding: utf-8 -*-

import random
from typing import Dict

import icon
import pytest
from icon.builder import Method
from icon.data import *
from icon.data.utils import hex_to_bytes
from icon.exception import HookException, SDKException
from icon.provider import HTTPProvider


class TestClient(object):
    @pytest.fixture(scope="class")
    def client(self):
        base_url = "https://ctz.solidwallet.io"
        provider = HTTPProvider(base_url, version=3)

        return icon.Client(provider)

    def test_get_total_supply(self, client):
        total_supply: int = client.get_total_supply()
        assert isinstance(total_supply, int)

    @pytest.mark.parametrize(
        "address, expected_balance",
        [
            ("hx1111111111111111111111111111111111111111", 0),
            ("hxffffffffffffffffffffffffffffffffffffffff", 0),
        ],
    )
    def test_get_balance(self, client, address, expected_balance):
        balance: int = client.get_balance(Address.from_string(address))
        assert balance == expected_balance

    @pytest.mark.parametrize(
        "block_height", [0, 1, 1_000_000, 10_000_000, 20_000_000, 30_000_000]
    )
    def test_get_block(self, client, block_height: int):
        block = client.get_block_by_height(block_height)
        assert isinstance(block, (Block, dict))

    @pytest.mark.parametrize(
        "tx_hash",
        [
            "0xbb0242d6b0d1d44b7c50cbfb22073a71343bc9565da18c3f29665bc86b9f0ca5",
            "0x423495f33b5b2c3755f5fad2426b0d79a10cd43ade10d89ef9057ef0d90fe54e",
        ],
    )
    def test_get_transaction(self, client, tx_hash: str):
        tx_hash: bytes = hex_to_bytes(tx_hash)
        tx: Transaction = client.get_transaction(tx_hash)
        assert tx.version == 3
        assert tx.nid == 1
        assert tx.tx_hash == tx_hash
        assert tx.block_height > 0
        assert isinstance(tx.block_hash, bytes) and len(tx.block_hash) == 32
        assert isinstance(tx.from_, Address)
        assert isinstance(tx.to, Address)
        assert isinstance(tx.value, int)
        assert tx.timestamp > 0

        print(tx)

    @pytest.mark.parametrize(
        "tx_hash",
        [
            "0xbb0242d6b0d1d44b7c50cbfb22073a71343bc9565da18c3f29665bc86b9f0ca5",
            "0x423495f33b5b2c3755f5fad2426b0d79a10cd43ade10d89ef9057ef0d90fe54e",
        ],
    )
    def test_get_transaction_result(self, client, tx_hash: str):
        tx_hash: bytes = hex_to_bytes(tx_hash)
        tx_result: TransactionResult = client.get_transaction_result(tx_hash)
        assert tx_result.status == TransactionResult.Status.SUCCESS
        assert tx_result.tx_hash == tx_hash

    def test_get_score_api(self, client):
        ret: Dict[str, str] = client.get_score_api(
            Address.from_int(AddressPrefix.CONTRACT, 0)
        )
        assert isinstance(ret, list)

    @pytest.mark.parametrize("hook_ret", [True, False])
    def test_request_hooks(self, dummy_provider, address, hook_ret):
        def hook(req: RpcRequest):
            assert req.method == Method.GET_BALANCE
            return hook_ret

        value = random.randint(0, 9999)
        dummy_response = RpcResponse(
            json_text={"jsonrpc": "2.0", "id": 0, "result": hex(value)}
        )

        dummy_provider.response = dummy_response
        client = icon.Client(dummy_provider)
        hooks = {"request": hook}

        if hook_ret:
            balance: int = client.get_balance(address, hooks=hooks)
            assert balance == value
        else:
            with pytest.raises(HookException) as exc_info:
                _: int = client.get_balance(address, hooks=hooks)

            e: HookException = exc_info.value
            assert e.code == SDKException.Code.HOOK_ERROR
            assert isinstance(e.user_data, RpcRequest)

            request: RpcRequest = e.user_data
            assert request.method == Method.GET_BALANCE
            assert request.params["address"] == str(address)

    @pytest.mark.parametrize("hook_ret", [True, False])
    def test_response_hooks(self, dummy_provider, address, hook_ret):
        def hook(res: RpcResponse):
            assert res.error is None
            assert isinstance(res.result, str)
            return hook_ret

        value = random.randint(0, 9999)
        dummy_response = RpcResponse(
            json_text={"jsonrpc": "2.0", "id": 0, "result": hex(value)}
        )

        dummy_provider.response = dummy_response
        client = icon.Client(dummy_provider)
        hooks = {"response": hook}

        if hook_ret:
            balance: int = client.get_balance(address, hooks=hooks)
            assert balance == value
        else:
            with pytest.raises(HookException) as exc_info:
                _: int = client.get_balance(address, hooks=hooks)

            e: HookException = exc_info.value
            assert e.code == SDKException.Code.HOOK_ERROR
            assert isinstance(e.user_data, RpcResponse)

            response: RpcResponse = e.user_data
            assert response == dummy_response
