# -*- coding: utf-8 -*-


import pytest
from icon.data.unit import icx, loop_to_str


@pytest.mark.parametrize(
    "value,result",
    [
        (0, "0"),
        (-0, "0"),
        (icx(1), "1.0"),
        (icx(-1), "-1.0"),
        (icx(100), f"100.0"),
        (icx(-100), f"-100.0"),
        (12345678, f"0.{'0' * 10}12345678"),
        (-12345678, f"-0.{'0' * 10}12345678"),
        (icx(10) + 1, f"10.{'0' * 17}1"),
        (icx(-10) - 1, f"-10.{'0' * 17}1"),
    ],
)
def test_loop_to_str(value, result):
    ret: str = loop_to_str(value)
    assert ret == result
