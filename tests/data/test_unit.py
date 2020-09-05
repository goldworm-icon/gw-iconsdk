# -*- coding: utf-8 -*-

import pytest

from icon.data import unit


class TestUnit(object):
    def test_icx(self):
        assert unit.icx(2) == 2 * 10 ** 18
