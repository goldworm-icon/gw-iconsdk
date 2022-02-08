# -*- coding: utf-8 -*-

import base64
import time
from typing import Dict, Union, List, Callable, Optional, Any
from urllib.parse import urlparse

from multimethod import multimethod

from . import builder
from .builder.key import Key
from .builder.method import Method
from .data.address import Address
from .data.block import Block
from .data.block_header import BlockHeader
from .data.rpc_request import RpcRequest
from .data.rpc_response import RpcResponse
from .data.transaction import Transaction, BaseTransaction, get_transaction
from .data.transaction_result import TransactionResult
from .data.utils import (
    bytes_to_hex,
    hex_to_bytes,
    str_to_int,
    to_str_dict,
)
from .data.validators import Validators
from .exception import (
    ArgumentException,
    HookException,
    JSONRPCException,
    SDKException,
)
from .provider.http_provider import HTTPProvider
from .provider.provider import Provider
from .utils.utils import generate_signature


class Client(object):
    _BLOCK_GENERATION_INTERVAL_MS = 2000

    def __init__(self, provider: Provider):
        self._provider = provider

    def get_block_by_hash(self, block_hash: bytes, **kwargs) -> Union[Block, Dict[str, Any]]:
        params = {"hash": bytes_to_hex(block_hash)}
        request = RpcRequest(Method.GET_BLOCK_BY_HASH, params)
        response = self.send_request(request, **kwargs)
        try:
            return Block.from_dict(response.result)
        except:
            return response.result

    def get_block_by_height(self, block_height: int, **kwargs) -> Union[Block, Dict[str, Any]]:
        if not (isinstance(block_height, int) and block_height >= 0):
            raise ValueError(f"Invalid params: {block_height}")

        params = {"height": hex(block_height)}
        request = RpcRequest(Method.GET_BLOCK_BY_HEIGHT, params)
        response = self.send_request(request, **kwargs)
        try:
            return Block.from_dict(response.result)
        except:
            return response.result

    def get_last_block(self, **kwargs) -> Union[Block, Dict[str, Any]]:
        request = RpcRequest(Method.GET_LAST_BLOCK)
        response = self.send_request(request, **kwargs)
        try:
            return Block.from_dict(response.result)
        except:
            return response.result

    def get_transaction(
            self, tx_hash: bytes, **kwargs
    ) -> Union[Transaction, BaseTransaction, Dict[str, Any]]:
        params = {"txHash": bytes_to_hex(tx_hash)}
        request = RpcRequest(Method.GET_TRANSACTION_BY_HASH, params)
        response = self.send_request(request, **kwargs)
        try:
            return get_transaction(response.result)
        except:
            return response.result

    def get_transaction_result(self, tx_hash: bytes, **kwargs) -> Union[TransactionResult, Dict[str, Any]]:
        params = {"txHash": bytes_to_hex(tx_hash)}
        request = RpcRequest(Method.GET_TRANSACTION_RESULT, params)
        response = self.send_request(request, **kwargs)
        try:
            return TransactionResult.from_dict(response.result)
        except:
            return response.result

    def get_transaction_result_with_timeout(self, tx_hash: bytes, **kwargs) -> Union[TransactionResult, Dict[str, Any]]:
        timeout_ms: int = kwargs.get("timeout_ms", 0)

        try_count = max(timeout_ms // self._BLOCK_GENERATION_INTERVAL_MS, 1)
        for i in range(try_count):
            time.sleep(self._BLOCK_GENERATION_INTERVAL_MS // 1000)

            try:
                return self.get_transaction_result(tx_hash, **kwargs)
            except SDKException as e:
                # If this is the last try
                if i == try_count - 1:
                    raise e

    def get_total_supply(self, **kwargs) -> int:
        request = RpcRequest(Method.GET_TOTAL_SUPPLY)
        response = self.send_request(request, **kwargs)
        return str_to_int(response.result)

    def get_balance(self, address: Address, **kwargs) -> int:
        params = {"address": str(address)}
        request = RpcRequest(Method.GET_BALANCE, params)
        response = self.send_request(request, **kwargs)
        return str_to_int(response.result)

    def get_score_api(self, address: Address, **kwargs) -> Dict[str, str]:
        params = {"address": str(address)}
        request = RpcRequest(Method.GET_SCORE_API, params)
        response = self.send_request(request, **kwargs)
        return response.result

    def get_block(
            self, value: Union[bytes, int, None] = None, **kwargs
    ) -> Dict[str, str]:
        if isinstance(value, bytes):
            params = {"hash": bytes_to_hex(value)}
        elif isinstance(value, int):
            params = {"hash": hex(value)}
        elif value is None:
            params = None
        else:
            raise ArgumentException(f"Invalid argument: {value}")

        request = RpcRequest(Method.GET_BLOCK, params)
        response = self.send_request(request, **kwargs)
        return response.result

    def send_transaction_and_wait(
            self, tx: Union[builder.Transaction, Dict[str, Any]], **kwargs
    ) -> Union[TransactionResult, Dict[str, Any]]:
        tx_hash: bytes = self.send_transaction(tx, **kwargs)
        return self.get_transaction_result_with_timeout(tx_hash, **kwargs)

    def send_transaction(self, tx: Union[builder.Transaction, Dict[str, Any]], **kwargs) -> bytes:
        if isinstance(tx, builder.Transaction):
            tx = tx.to_dict()

        private_key: Optional[bytes] = kwargs.get("private_key")
        if isinstance(private_key, bytes):
            tx: Dict[str, str] = to_str_dict(tx)
            tx[Key.SIGNATURE] = generate_signature(tx, private_key)

        if Key.SIGNATURE not in tx:
            raise ArgumentException(f"Signature not found")

        request = RpcRequest(Method.SEND_TRANSACTION, tx)
        response = self.send_request(request, **kwargs)
        return hex_to_bytes(response.result)

    def call(self, params: Dict[str, Any], **kwargs) -> Union[str, Dict[str, str]]:
        request = RpcRequest(Method.CALL, params)
        response = self.send_request(request, **kwargs)
        return response.result

    def estimate_step(self, tx: Union[builder.Transaction, Dict[str, Any]], **kwargs) -> int:
        if isinstance(tx, builder.Transaction):
            tx = tx.to_dict()

        if Key.STEP_LIMIT in tx:
            del tx[Key.STEP_LIMIT]
        if Key.SIGNATURE in tx:
            del tx[Key.SIGNATURE]

        request = RpcRequest(Method.ESTIMATE_STEP, tx)
        response = self.send_request(request, **kwargs)
        return str_to_int(response.result)

    def get_status(self, **kwargs) -> Dict[str, str]:
        params = {"filter": ["lastBlock"]}
        request = RpcRequest(Method.GET_STATUS, params)
        response = self.send_request(request, **kwargs)
        return response.result

    def get_account(self, address: Address, _filter: int, **kwargs) -> Dict[str, str]:
        params = {"address": str(address), "filter": hex(_filter)}
        request = RpcRequest(Method.GET_ACCOUNT, params)
        response = self.send_request(request, **kwargs)
        return response.result

    @multimethod
    def send_request(self, request: RpcRequest, **kwargs) -> RpcResponse:
        hooks: Dict[str, Union[Callable, List[Callable]]] = kwargs.get("hooks")

        # hooks for request
        ret: bool = self._dispatch_hook("request", hooks, request)
        if not ret:
            raise HookException(f"request hooks stopped", request)

        response = self._provider.send(request)

        # hooks for response
        ret: bool = self._dispatch_hook("response", hooks, response)
        if not ret:
            raise HookException(f"response hooks stopped", response)

        if response.error:
            raise JSONRPCException(f"{response.error}", response)

        return response

    @multimethod
    def send_request(
            self, method: str, params: Dict[str, str], **kwargs
    ) -> RpcResponse:
        request = RpcRequest(method, params)
        return self.send_request(request, **kwargs)

    @classmethod
    def _dispatch_hook(cls, key: str, hooks, hook_data: Union[RpcRequest, RpcResponse]):
        hooks = hooks or {}
        hooks = hooks.get(key)

        if hooks:
            if hasattr(hooks, "__call__"):
                hooks = [hooks]

            for hook in hooks:
                ret: Optional[bool] = hook(hook_data)
                if ret is False:
                    return False

        return True

    def get_data_by_hash(self, data_hash: bytes, **kwargs) -> bytes:
        params = {"hash": bytes_to_hex(data_hash)}
        request = RpcRequest(Method.GET_DATA_BY_HASH, params)
        response = self.send_request(request, **kwargs)
        return base64.standard_b64decode(response.result)

    def get_block_header_by_height(self, height: int, **kwargs) -> bytes:
        params = {"height": hex(height)}
        request = RpcRequest(Method.GET_BLOCK_HEADER_BY_HEIGHT, params)
        response = self.send_request(request, **kwargs)
        return base64.standard_b64decode(response.result)

    def get_votes_by_height(self, height: int, **kwargs) -> bytes:
        params = {"height": hex(height)}
        request = RpcRequest(Method.GET_VOTES_BY_HEIGHT, params)
        response = self.send_request(request, **kwargs)
        return base64.standard_b64decode(response.result)

    def get_validators_by_height(self, height: int, **kwargs) -> Validators:
        bs: bytes = self.get_block_header_by_height(height - 1, **kwargs)
        block_header = BlockHeader.from_bytes(bs)

        bs = self.get_data_by_hash(block_header.next_validators_hash, **kwargs)
        return Validators.from_bytes(bs)


class ClientEx()


def create_client(url: str, version: int = 3) -> Client:
    o = urlparse(url)
    return Client(HTTPProvider(f"{o.scheme}://{o.netloc}", version))
