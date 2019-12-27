#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: kaivean
# Mail: kaivean@outlook.com
# usage test: rm -fr dist && python setup.py sdist  && twine upload --repository-url https://test.pypi.org/legacy/ dist/uaDevice-*.tar.gz
# usage: rm -fr dist && python setup.py sdist  && twine upload dist/uaDevice-*.tar.gz
#############################################

import os
from setuptools import setup, find_packages
ROOT = os.path.dirname(os.path.realpath(__file__))

setup(
    name = "uaDevice",
    version = "1.0.3",
    keywords = ("ua", "user-agent", "User Agent", "parser", "device", "os", "browser", "engine", "data analysis", "china", "中国", "国内"),
    description = "User Agent parser, More accurate",
    long_description = open(os.path.join(ROOT, 'README.md')).read(),
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
