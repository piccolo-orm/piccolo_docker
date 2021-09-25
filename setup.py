#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup

from dockerdb import __VERSION__ as VERSION

directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(directory, "README.md")) as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="piccolo_docker",
    version=VERSION,
    description=("Easily spin up databases for your Piccolo project using Docker"),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Antonio One",
    author_email="antonio.one@pm.me",
    python_requires=">=3.8.0",
    url="https://github.com/piccolo-orm/piccolo_docker",
    packages=find_packages(exclude=("tests",)),
    package_data={
        "": [
            "templates/*",
            "templates/**/*",
            "templates/**/**/*",
            "templates/**/**/**/*",
        ],
        "piccolo": ["py.typed"],
    },
    install_requires="requirements.txt",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: AsyncIO",
        "Typing :: Typed",
        "Topic :: Database",
    ],
    entry_points={"console_scripts": ["piccolo = piccolo.main:main"]},
)
