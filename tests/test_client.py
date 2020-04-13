# -*- coding: utf-8 -*-

import icon
import pytest
from icon.data.address import Address
from icon.data.transaction import Transaction
from icon.data.transaction_result import TransactionResult
from icon.utils.convert_type import hex_to_bytes


class TestClient(object):
    @pytest.fixture(scope="class")
    def client(self):
        base_url = "https://ctz.solidwallet.io"
        provider = icon.HTTPProvider(base_url, version=3)

        return icon.Client(provider)

    def test_get_total_supply(self, client):
        total_supply: int = client.get_total_supply()
        assert isinstance(total_supply, int)

    @pytest.mark.parametrize(
        "address, expected_balance",
        [
            ("hx1b8959dd5c57d2c502e22ee0a887d33baec09091", 907_829_600_000_000_000),
            ("hxffffffffffffffffffffffffffffffffffffffff", 0),
        ],
    )
    def test_get_balance(self, client, address, expected_balance):
        balance: int = client.get_balance(Address.from_string(address))
        assert balance == expected_balance

    @pytest.mark.parametrize(
        "tx_hash",
        [
            "0xbb0242d6b0d1d44b7c50cbfb22073a71343bc9565da18c3f29665bc86b9f0ca5",
            "0x423495f33b5b2c3755f5fad2426b0d79a10cd43ade10d89ef9057ef0d90fe54e",
        ],
    )
    def test_get_transaction(self, client, tx_hash: str):
        tx_hash: bytes = hex_to_bytes(tx_hash)
        tx: "Transaction" = client.get_transaction(tx_hash)
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
        tx_result: "TransactionResult" = client.get_transaction_result(tx_hash)
        assert tx_result.status == TransactionResult.Status.SUCCESS
        assert tx_result.tx_hash == tx_hash
