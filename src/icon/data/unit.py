# -*- coding: utf-8 -*-

ICX_TO_LOOP = 10 ** 18
LOOP_TO_ISCORE = 1000


def icx(value: int) -> int:
    return value * ICX_TO_LOOP


def loop_to_str(value: int) -> str:
    if value == 0:
        return "0"

    sign: str = "-" if value < 0 else ""
    integer, exponent = divmod(abs(value), ICX_TO_LOOP)
    if exponent == 0:
        return f"{sign}{integer}.0"

    return f"{sign}{integer}.{exponent:018d}"


def loop_to_iscore(value: int) -> int:
    return value * LOOP_TO_ISCORE
