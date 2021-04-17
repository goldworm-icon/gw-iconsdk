# -*- coding: utf-8 -*-

import os

from icon.utils.in_memory_zip import InMemoryZip


def test_in_memory_zip():
    parent_path: str = os.path.dirname(__file__)
    path: str = os.path.join(parent_path, "data_to_zip")

    mem_zip = InMemoryZip()
    mem_zip.run(path)

    with open("data.zip", "wb") as f:
        f.write(mem_zip.data)
