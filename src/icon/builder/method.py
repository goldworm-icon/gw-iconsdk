# -*- coding: utf-8 -*-


class Method(object):
    """JSON-RPC METHODS supported by ICON
    """

    CALL = "icx_call"

    GET_BLOCK_BY_HASH = "icx_getBlockByHash"
    GET_BLOCK_BY_HEIGHT = "icx_getBlockByHeight"
    GET_LAST_BLOCK = "icx_getLastBlock"

    GET_TRANSACTION_BY_HASH = "icx_getTransactionByHash"
    GET_TRANSACTION_RESULT = "icx_getTransactionResult"

    GET_BALANCE = "icx_getBalance"
    GET_SCORE_API = "icx_getScoreApi"
    GET_TOTAL_SUPPLY = "icx_getTotalSupply"

    ESTIMATE_STEP = "debug_estimateStep"
    SEND_TRANSACTION = "icx_sendTransaction"
