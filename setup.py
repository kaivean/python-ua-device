#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mage
# Mail: mage@woodcol.com
# Created Time:  2018-1-23 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
    name = "uaDevice",
    version = "1.0.0",
    keywords = ("ua", "user-agent", "User Agent", "parser", "device", "os", "browser", "engine", "data analysis", "china", "中国", "国内"),
    description = "User Agent parser, More accurate",
    long_description = "User Agent parser, More accurate",
    license = "MIT Licence",

    url = "https://github.com/kaivean/python-ua-device",
    author = "kaivean",
    author_email = "kaivean@outlook.com",

    packages = find_packages('src', exclude=['*.test', '*.test.*', 'test.*', 'test', 'test.py']),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)
