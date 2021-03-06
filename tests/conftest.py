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

import os
import time
from typing import Callable

import pytest
from icon.data import Address, AddressPrefix
from icon.data import RpcRequest, RpcResponse
from icon.provider import Provider
from icon.wallet import KeyWallet


@pytest.fixture(scope="function")
def tx_hash() -> bytes:
    """Returns 32 length random tx_hash in bytes

    :return: tx_hash in bytes
    """
    print("tx_hash()")
    return os.urandom(32)


@pytest.fixture(scope="function")
def block_hash() -> bytes:
    """Returns 32 length random block_hash in bytes

    :return: block_hash in bytes
    """
    print("block_hash()")
    return os.urandom(32)


@pytest.fixture(scope="function")
def address() -> Address:
    return Address(AddressPrefix.EOA, os.urandom(20))


@pytest.fixture(scope="session")
def create_address() -> Callable[[], Address]:
    def func():
        return Address(AddressPrefix.EOA, os.urandom(20))

    return func


@pytest.fixture
def step_price() -> int:
    return 10 ** 10


@pytest.fixture
def timestamp() -> int:
    """Returns random timestamp in microseconds
    """
    return int(time.time() * 10 ** 6)


@pytest.fixture
def logs_bloom() -> bytes:
    return os.urandom(256)


@pytest.fixture
def wallet() -> KeyWallet:
    return KeyWallet()


class DummyProvider(Provider):
    def __init__(self):
        self._response = None

    @property
    def response(self) -> RpcResponse:
        return self._response

    @response.setter
    def response(self, value: RpcResponse):
        self._response = value

    def send(self, request: RpcRequest) -> RpcResponse:
        return self._response


@pytest.fixture
def dummy_provider():
    return DummyProvider()
