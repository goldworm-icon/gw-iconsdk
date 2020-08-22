# -*- coding: utf-8 -*-

from base64 import standard_b64decode

from icon.builder import Transaction
from icon.builder.key import Key
from icon.builder.transaction_builder import TransactionBuilder
from icon.wallet import KeyWallet


def test_transaction_builder(wallet: KeyWallet, address):
    tx: Transaction = (
        TransactionBuilder()
        .from_(wallet.address)
        .to(address)
        .value(100)
        .nid(1)
        .step_limit(1_000_000)
        .build()
    )

    signature: bytes = tx.sign(wallet.private_key)
    assert wallet.verify_signature(signature, tx.tx_hash)

    signature_in_tx = standard_b64decode(tx[Key.SIGNATURE])
    assert signature_in_tx == signature
