# -*- coding: utf-8 -*-

from enum import Flag, auto


class Key(object):
    VERSION = "version"
    NID = "nid"
    FROM = "from"
    TO = "to"
    VALUE = "value"
    STEP_LIMIT = "stepLimit"
    TIMESTAMP = "timestamp"
    NONCE = "nonce"
    DATA_TYPE = "dataType"
    DATA = "data"
    SIGNATURE = "signature"


class KeyFlag(Flag):
    NONE = 0

    VERSION = auto()
    NID = auto()
    FROM = auto()
    TO = auto()
    VALUE = auto()
    STEP_LIMIT = auto()
    TIMESTAMP = auto()
    NONCE = auto()
    DATA_TYPE = auto()
    DATA = auto()
    SIGNATURE = auto()
