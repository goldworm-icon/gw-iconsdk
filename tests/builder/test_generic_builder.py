# -*- coding: utf-8 -*-

from icon.builder.generic_builder import GenericBuilder
from icon.builder.method import Method
from icon.data.rpc_request import RpcRequest


class TestGenericBuilder(object):
    def test_build(self):
        builder = GenericBuilder(Method.GET_TOTAL_SUPPLY)
        request = builder.build()
        assert isinstance(request, RpcRequest)

        print(request)
