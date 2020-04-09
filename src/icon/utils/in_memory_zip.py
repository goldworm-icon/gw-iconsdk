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
from typing import Optional
from zipfile import ZipFile, ZIP_DEFLATED

from ..constant import PACKAGE_JSON_FILE
from ..data.exception import ZipException


def gen_deploy_data_content(path: str) -> bytes:
    """Generate bytes of zip data of SCORE.

    :param path: Path of the directory to be zipped.
    """
    if not os.path.isdir(path) and not os.path.isfile(path):
        raise ValueError(f"Invalid path {path}")

    memory_zip = InMemoryZip()
    memory_zip.run(path)

    return memory_zip.data


class InMemoryZip(object):
    """Class for compressing data in memory using zip and BytesIO."""

    def __init__(self):
        self._in_memory: Optional[BytesIO] = BytesIO()

    @property
    def data(self) -> bytes:
        """Returns zip data

        :return: zip data
        """
        return self._in_memory.getvalue()

    def run(self, path: str, archive_root: str = "score"):
        if os.path.isfile(path):
            self._run_with_file(path)
        elif os.path.isdir(path):
            self._run_with_dir(path, archive_root)
        else:
            raise ZipException(f"Invalid SCORE path: {path}")

    def _run_with_file(self, path: str):
        zf = ZipFile(path, "r", ZIP_DEFLATED, allowZip64=False)
        zf.testzip()

        with open(path, mode="rb") as fp:
            self._in_memory.seek(0)
            self._in_memory.write(fp.read())

    def _run_with_dir(self, path: str, archive_root: str):
        path: str = os.path.abspath(path)
        score_root: str = self.find_score_root(path, PACKAGE_JSON_FILE)

        with ZipFile(self._in_memory, "w", ZIP_DEFLATED, allowZip64=False) as zf:
            for root, dirs, files in os.walk(score_root):
                dirname: str = os.path.basename(root)
                if not self._is_dirname_valid(dirname):
                    continue

                arc_root: str = root.replace(score_root, archive_root)

                for file in files:
                    if self._is_filename_valid(file):
                        full_path: str = os.path.join(root, file)
                        arcname: str = os.path.join(arc_root, file)
                        zf.write(full_path, arcname)

    @staticmethod
    def find_score_root(path: str, filename: str) -> str:
        """Find the directory where a given file is located

        If path

        :param path:
        :param filename:
        :return:
        """

        for root, dirs, files in os.walk(path):
            if filename in files:
                return root

        raise ZipException(f"{filename} not found")

    @staticmethod
    def _is_filename_valid(filename: str) -> bool:
        if filename.startswith("."):
            return False
        if filename == PACKAGE_JSON_FILE:
            return True

        return filename.endswith(".py")

    @staticmethod
    def _is_dirname_valid(dirname: str) -> bool:
        excluded_dirnames = ("__pycache__", "tests")

        if dirname.startswith("."):
            return False
        if dirname in excluded_dirnames:
            return False

        return True
