# coding: utf-8

import setuptools


setuptools.setup(
    name='jason',
    version='0.0.6',
    install_requires=[
        "Flask==1.0.2"
    ],
    extras_require={
        'dev': [
            'pytest==4.4.1'
        ]
    },
    packages=setuptools.find_packages()
)
