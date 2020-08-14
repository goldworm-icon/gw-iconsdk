# -*- coding: utf-8 -*-

import pytest

from icon.data.address import Address
from icon.utils.type import to_str_dict, bytes_to_hex


class TestConvertType(object):
    @pytest.fixture
    def address(self):
        return Address.from_string("hx287faae3e929cdeb8cd1f68be713595b47f3c0d3")

    def test_to_str_dict(self, address):
        d = {
            "version": 0,
            "name": "apple",
            "on": False,
            "data": b"hello",
            "address": address,
            "list": [0, True, "hello", b"good", address],
            "params": {"name": "banana", "age": 20, "single": True, "address": address},
        }

        expected = {
            "version": hex(d["version"]),
            "name": d["name"],
            "on": hex(int(d["on"])),
            "data": bytes_to_hex(d["data"]),
            "address": str(address),
            "list": [hex(0), hex(True), "hello", bytes_to_hex(b"good"), str(address)],
            "params": {
                "name": d["params"]["name"],
                "age": hex(d["params"]["age"]),
                "single": hex(d["params"]["single"]),
                "address": str(address),
            },
        }

        ret = to_str_dict(d)
        assert ret == expected
