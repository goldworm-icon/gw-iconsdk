# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import environ, path

version = environ.get("VERSION")

if version is None:
    with open(path.join(".", "VERSION")) as version_file:
        version = version_file.read().strip()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="gwiconsdk",
    version=version,
    package_dir={"": "src"},
    description="Python version IconSDK made by goldworm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="goldworm",
    author_email="goldworm@iconloop.com",
    url="https://github.com/goldworm-icon/gw-iconsdk",
    packages=find_packages(exclude=["tests*"]),
    test_suite="tests",
    install_requires=[
         "eth-keyfile>=0.5.1",
         "secp256k1>=0.13.2",
         "multipledispatch>=0.5.0",
         "requests>=2.20.0"
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    license="Apache License 2.0",
    classifiers=[
         "Development Status :: 5 - Production/Stable",
         "Intended Audience :: Developers",
         "Intended Audience :: System Administrators",
         "Natural Language :: English",
         "License :: OSI Approved :: Apache Software License",
         "Programming Language :: Python",
         "Programming Language :: Python :: 3.6"
         "Programming Language :: Python :: 3.7"
     ]
)
