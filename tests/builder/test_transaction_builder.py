# -*- coding: utf-8 -*-

from typing import Dict

from icon.builder.transaction_builder import TransactionBuilder
from icon.wallet.wallet import KeyWallet


def test_transaction_builder(wallet: KeyWallet, address):
    builder = TransactionBuilder()
    builder.version(3)
    builder.from_(wallet.address)
    builder.to(address)
    builder.value(100)
    builder.nid(1)
    builder.step_limit(1_000_000)

    tx: Dict[str, str] = builder.build_and_sign(wallet.private_key)
    print(tx)
