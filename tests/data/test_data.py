# -*- coding: utf-8 -*-

# Copyright 2019 ICON Foundation
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

import pytest
from icon.data.address import Address
from icon.data.dict import Dict
from icon.data.primitive import Bytes, Int, Bool


@pytest.mark.skip
class TestPrimitiveData(object):

    def test_int(self):
        value: int = 100
        int_object = Int(value)
        assert int_object.value == value
        assert int(int_object) == value

        value: int = 200
        int_object.value = value
        assert int_object.value == value
        assert int(int_object) == value

    def test_int_type_error(self):
        with pytest.raises(TypeError):
            int_object = Int("hello")
            int_object.value = 100

        int_object = Int(100)
        with pytest.raises(TypeError):
            int_object.value = "abc"

    def test_dict(self):
        params = Dict()
        params["value"] = 100
        params["string"] = "hello"
        params["bytes"] = Bytes(b"hello")
        params["data"] = {
            "method": "call",
            "params": {
                "address": Address.from_string("hxb31a79f6f53af0d524176d5ab0251556b69c87b6"),
                "name": "apple",
                "values": [Int(0), Int(1), Int(2)],
                "on": Bool(True),
                "off": Bool(False)
            }
        }

        print(str(params))
        print('{"value":"0x64"}')
