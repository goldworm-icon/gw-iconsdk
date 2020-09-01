# -*- coding: utf-8 -*-

from typing import Dict, Union, List, Callable, Optional

from multimethod import multimethod

from . import builder
from .builder.method import Method
from .data.address import Address
from .data.block import Block
from .data.rpc_request import RpcRequest
from .data.rpc_response import RpcResponse
from .data.transaction import Transaction
from .data.transaction_result import TransactionResult
from .data.utils import str_to_int, bytes_to_hex, hex_to_bytes
from .exception import (
    ArgumentException,
    HookException,
    JSONRPCException,
)
from .provider.provider import Provider


class Client(object):
    def __init__(self, provider: Provider):
        self._provider = provider

    def get_block_by_hash(self, block_hash: bytes, **kwargs) -> Block:
        params = {"hash": bytes_to_hex(block_hash)}
        request = RpcRequest(Method.GET_BLOCK_BY_HASH, params)
        response = self.send_request(request, **kwargs)
        return Block.from_dict(response.result)

    def get_block_by_height(self, block_height: int, **kwargs) -> Block:
        if not (isinstance(block_height, int) and block_height >= 0):
            raise ValueError(f"Invalid params: {block_height}")

        params = {"height": hex(block_height)}
        request = RpcRequest(Method.GET_BLOCK_BY_HEIGHT, params)
        response = self.send_request(request, **kwargs)
        return Block.from_dict(response.result)

    def get_last_block(self, **kwargs) -> Block:
        request = RpcRequest(Method.GET_LAST_BLOCK)
        response = self.send_request(request, **kwargs)
        return Block.from_dict(response.result)

    def get_transaction(self, tx_hash: bytes, **kwargs) -> Transaction:
        params = {"txHash": bytes_to_hex(tx_hash)}
        request = RpcRequest(Method.GET_TRANSACTION_BY_HASH, params)
        response = self.send_request(request, **kwargs)
        return Transaction.from_dict(response.result)

    def get_transaction_result(self, tx_hash: bytes, **kwargs) -> TransactionResult:
        params = {"txHash": bytes_to_hex(tx_hash)}
        request = RpcRequest(Method.GET_TRANSACTION_RESULT, params)
        response = self.send_request(request, **kwargs)
        return TransactionResult.from_dict(response.result)

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

    def send_transaction(self, tx: builder.Transaction, **kwargs) -> Union[int, bytes]:
        if not isinstance(tx, builder.Transaction):
            ValueError(f"Invalid params: tx={tx}")

        private_key: Optional[bytes] = kwargs.get("private_key")
        if isinstance(private_key, bytes):
            tx.sign(private_key)

        if kwargs.get("estimate", False):
            ret: int = self.estimate_step(tx, **kwargs)
        else:
            ret: bytes = self._send_transaction(tx, **kwargs)

        return ret

    def _send_transaction(self, tx: builder.Transaction, **kwargs) -> bytes:
        request = RpcRequest(Method.SEND_TRANSACTION, tx.to_dict())
        response = self.send_request(request, **kwargs)
        return hex_to_bytes(response.result)

    def call(self, params: Dict[str, str], **kwargs) -> Union[str, Dict[str, str]]:
        request = RpcRequest(Method.CALL, params)
        response = self.send_request(request, **kwargs)
        return response.result

    def estimate_step(self, tx: builder.Transaction, **kwargs) -> int:
        request = RpcRequest(Method.ESTIMATE_STEP, tx.to_dict())
        response = self.send_request(request, **kwargs)
        return str_to_int(response.result)

    def get_status(self, **kwargs) -> Dict[str, str]:
        params = {"filter": ["lastBlock"]}
        request = RpcRequest(Method.GET_STATUS, params)
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
                ret: bool = hook(hook_data)
                if not ret:
                    return False

        return True
