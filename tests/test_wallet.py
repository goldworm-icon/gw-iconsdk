# -*- coding: utf-8 -*-

import os

import pytest
from icon.data import Address
from icon.exception import KeyStoreException
from icon.wallet import LightWallet, KeyWallet, Wallet

ROOT_PATH: str = os.path.dirname(__file__)
KEYFILE_PATH: str = os.path.join(ROOT_PATH, "test.key")


@pytest.fixture
def light_wallet() -> Wallet:
    path = KEYFILE_PATH
    return LightWallet.from_path(path)


@pytest.fixture
def key_wallet() -> Wallet:
    path = KEYFILE_PATH
    return KeyWallet.load(path, password="test1_Account")


@pytest.fixture
def address() -> Address:
    return Address.from_string("hxe7af5fcfd8dfc67530a01a0e403882687528dfcb")


class TestLightWallet:
    def test_address(self, light_wallet, address):
        assert light_wallet.address == address

    def test_private_key(self, light_wallet):
        with pytest.raises(KeyStoreException):
            print(light_wallet.private_key)

    def test_public_key(self, light_wallet):
        with pytest.raises(KeyStoreException):
            print(light_wallet.public_key)

    def test_load(self, light_wallet):
        wallet = LightWallet.load(KEYFILE_PATH)
        assert wallet == light_wallet

    @pytest.mark.parametrize("recoverable", (True, False))
    def test_sign(self, light_wallet, recoverable):
        message_hash: bytes = os.urandom(32)
        with pytest.raises(KeyStoreException):
            light_wallet.sign(message_hash, recoverable=recoverable)

    def test_verify_signature(self, light_wallet):
        signature: bytes = os.urandom(65)
        message_hash: bytes = os.urandom(32)
        with pytest.raises(KeyStoreException):
            light_wallet.verify_signature(signature, message_hash)


class TestKeyWallet:
    def test_address(self, key_wallet, address):
        assert key_wallet.address == address

    def test_private_key(self, key_wallet):
        assert isinstance(key_wallet.private_key, bytes)
        assert len(key_wallet.private_key) == 32

    def test_public_key(self, key_wallet):
        public_key: bytes = key_wallet.public_key
        assert isinstance(public_key, bytes)
        assert len(public_key) == 65
