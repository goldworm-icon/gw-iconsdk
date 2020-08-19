# -*- coding: utf-8 -*-

import json
import os
from abc import ABCMeta, abstractmethod

from eth_keyfile import create_keyfile_json, extract_key_from_keyfile

from ..data.address import Address
from icon.exception import KeyStoreException
from ..utils.crypto import sign, verify_signature, create_key_pair
from ..utils.utils import is_keystore_valid


class Wallet(metaclass=ABCMeta):
    """An interface `Wallet` has 2 abstract methods, `get_address()` and `sign(hash: str)`."""

    @abstractmethod
    def address(self) -> Address:
        pass

    @abstractmethod
    def sign(self, message_hash: bytes, recoverable: bool) -> bytes:
        """Generates signature from input data which is transaction data

        :param message_hash: 32-byte message_hash to sign
        :param recoverable: recoverable signature or not
        :return signature: signature made from data and private key
        """
        pass

    @abstractmethod
    def verify_signature(self, signature: bytes, message_hash: bytes) -> bool:
        pass


class KeyWallet(Wallet):
    """KeyWallet class implements Wallet."""

    def __init__(self, private_key: bytes = None):
        self._private_key, self._public_key = create_key_pair(private_key)
        self._address = Address.from_public_key(self._public_key)

    @property
    def private_key(self) -> bytes:
        return self._private_key

    @property
    def public_key(self) -> bytes:
        return self._public_key

    @property
    def address(self) -> Address:
        return self._address

    @staticmethod
    def load(file_path: str, password: str) -> "KeyWallet":
        """Loads a wallet from a keystore file with your password and generates an instance of Wallet.

        :param file_path: File path of the keystore file. type(str)
        :param password:
            Password for the keystore file.
            It must include alphabet character, number, and special character.
        :return: An instance of Wallet class.
        """
        try:
            with open(file_path, "rb") as file:
                private_key: bytes = extract_key_from_keyfile(
                    file, bytes(password, "utf-8")
                )
                return KeyWallet(private_key)
        except FileNotFoundError:
            raise KeyStoreException("File is not found.")
        except ValueError:
            raise KeyStoreException("Password is wrong.")
        except Exception as e:
            raise KeyStoreException(f"keystore file error.{e}")

    def save(self, path: str, password: str):
        """Stores data of an instance of a derived wallet class on the file path with your password.

        :param path: File path of the keystore file. type(str)
        :param password:
            Password for the keystore file. Password must include alphabet character, number, and special character.
            type(str)
        """
        try:
            if os.path.isfile(path):
                raise KeyStoreException("File already exists")

            keystore: dict = create_keyfile_json(
                self._private_key,
                password.encode("utf-8"),
                iterations=16384,
                kdf="scrypt",
            )
            keystore["address"] = str(self._address)
            keystore["coinType"] = "icx"

            # validate the contents of a keystore file.
            if not is_keystore_valid(keystore):
                raise KeyStoreException("Invalid keystore")

            with open(path, "wt") as f:
                text: str = json.dumps(keystore)
                f.write(text)

        except PermissionError:
            raise KeyStoreException("Not enough permission")
        except FileNotFoundError:
            raise KeyStoreException("File not found")
        except IsADirectoryError:
            raise KeyStoreException("Directory is invalid")

    def sign(self, message_hash: bytes, recoverable: bool) -> bytes:
        """Generates signature with message_hash

        :param message_hash: 32-byte hash data
        :param recoverable: If it is True, recoverable signature will be generated
        :return signature: signature made from input
        """
        return sign(message_hash, self._private_key, recoverable)

    def verify_signature(self, signature: bytes, message_hash: bytes) -> bool:
        return verify_signature(signature, message_hash, self._public_key)
