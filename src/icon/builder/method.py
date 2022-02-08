# -*- coding: utf-8 -*-


class Method(object):
    """JSON-RPC METHODS supported by ICON
    """

    CALL = "icx_call"

    GET_BLOCK = "icx_getBlock"
    GET_BLOCK_BY_HASH = "icx_getBlockByHash"
    GET_BLOCK_BY_HEIGHT = "icx_getBlockByHeight"
    GET_LAST_BLOCK = "icx_getLastBlock"

    GET_TRANSACTION_BY_HASH = "icx_getTransactionByHash"
    GET_TRANSACTION_RESULT = "icx_getTransactionResult"

    GET_BALANCE = "icx_getBalance"
    GET_SCORE_API = "icx_getScoreApi"
    GET_TOTAL_SUPPLY = "icx_getTotalSupply"

    ESTIMATE_STEP = "debug_estimateStep"
    GET_ACCOUNT = "debug_getAccount"

    SEND_TRANSACTION = "icx_sendTransaction"

    GET_STATUS = "ise_getStatus"

    # Extended
    GET_DATA_BY_HASH = "icx_getDataByHash"
    GET_BLOCK_HEADER_BY_HEIGHT = "icx_getBlockHeaderByHeight"
    GET_VOTES_BY_HEIGHT = "icx_getVotesByHeight"
    GET_PROOF_FOR_RESULT = "icx_getProofForResult"
    GET_PROOF_FOR_EVENT = "icx_getProofForEvent"
