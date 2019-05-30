# -*- coding: utf-8 -*-
# Copyright 2018 ICON Foundation
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

import os
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED

from ..exception import ZipException


def gen_deploy_data_content(path: str) -> bytes:
    """Generate bytes of zip data of SCORE.

    :param path: Path of the directory to be zipped.
    """
    if not os.path.isdir(path) and not os.path.isfile(path):
        raise ValueError(f"Invalid path {path}")

    memory_zip = InMemoryZip()
    memory_zip.zip_in_memory(path)

    return memory_zip.data


class InMemoryZip:
    """Class for compressing data in memory using zip and BytesIO."""

    def __init__(self):
        self._in_memory = BytesIO()

    @property
    def data(self) -> bytes:
        """Returns zip data

        :return: zip data
        """
        return self._in_memory.getvalue()

    def zip_in_memory(self, path: str):
        """Compress zip data (bytes) in memory.

        :param path: The path of the directory to be zipped.
        """
        try:
            path: str = os.path.abspath(path)

            # when it is a zip file
            if os.path.isfile(path):
                zf = ZipFile(path, "r", ZIP_DEFLATED, allowZip64=False)
                zf.testzip()
                with open(path, mode="rb") as fp:
                    self._in_memory.seek(0)
                    self._in_memory.write(fp.read())
            else:
                # root path for figuring out directory of tests
                with ZipFile(self._in_memory, "a", ZIP_DEFLATED, False) as zf:
                    for root, folders, files in os.walk(path):
                        for file in files:
                            full_path: str = os.path.join(root, file)
                            zf.write(full_path)
        except ZipException:
            raise ZipException

