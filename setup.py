#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: kaivean
# Mail: kaivean@outlook.com
# 1: modify following version
# 2. build and upload
#   usage test: rm -fr dist && python3 setup.py sdist  && twine upload --repository-url https://test.pypi.org/legacy/ dist/uaDevice-*.tar.gz
#   usage: rm -fr dist && python3 setup.py sdist  && twine upload dist/uaDevice-*.tar.gz
#############################################

import os
from setuptools import setup, find_packages
ROOT = os.path.dirname(os.path.realpath(__file__))

import sys
import re
import os
import json

if sys.version_info < (3, 0):
    desc = open(os.path.join(ROOT, 'README.md')).read()
else:
    desc = open(os.path.join(ROOT, 'README.md'), encoding='UTF-8').read()

setup(
    name = "uaDevice",
    version = "1.0.12",
    keywords = ("ua", "user-agent", "User Agent", "parser", "device", "os", "browser", "engine", "data analysis", "china", "中国", "国内"),
    description = "User Agent parser, More accurate",
    long_description = desc,
    long_description_content_type="text/markdown",
    license = "MIT Licence",

    url = "https://github.com/kaivean/python-ua-device",
    author = "kaivean",
    author_email = "kaivean@outlook.com",

    packages = find_packages(exclude=['*.test', '*.test.*', 'test.*', 'test', 'test.py']),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)
