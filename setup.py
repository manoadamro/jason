# coding: utf-8

import setuptools


NAME = 'jason'
VERSION = '0.0.4'
REQUIRES = [
    "Flask==1.0.2"
]


setuptools.setup(
    name=NAME,
    version=VERSION,
    install_requires=REQUIRES,
    packages=setuptools.find_packages()
)
