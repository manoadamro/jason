# coding: utf-8

import setuptools


setuptools.setup(
    name='jason',
    version='0.0.6',
    install_requires=[
        "Flask==1.0.2",
        "PyJWT==1.7.1"
    ],
    extras_require={
        'dev': [
            'pytest==4.4.1',
            'isort==4.3.4',
            'black==18.9b0',
            'coverage==4.5.1'
        ]
    },
    packages=setuptools.find_packages()
)
