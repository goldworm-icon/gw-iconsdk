# -*- coding: utf-8 -*-

from icon.builder.transaction_builder import TransactionBuilder, Transaction
from icon.data.address import AddressPrefix, Address
from icon.utils.serializer import generate_message


class TestSerializer(object):
    def test_generate_message(self, wallet):
        builder = TransactionBuilder()
        builder.version(3).nid(1).from_(wallet.address).to(
            Address.from_int(AddressPrefix.CONTRACT, 0)
        ).value(0).step_limit(1_000_000).nonce(0)

        tx: Transaction = builder.build()
        message: str = generate_message(tx.to_dict())
        assert isinstance(message, str)
        assert message.startswith("icx_sendTransaction")
