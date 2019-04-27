# coding: utf-8

import setuptools


setuptools.setup(
    name='jason',
    version='0.1.0',
    install_requires=[
        'fire==0.1.3',
        "Flask==1.0.2",
        "jsonpointer==2.0",
        'pika==0.13.1',
        "pycryptodome==3.8.1",
        "PyJWT==1.7.1",
        'redis==3.2.1',
        'SQLAlchemy==1.2.18',
        'waitress==1.2.1',
    ],
    extras_require={
        'dev': [
            'black==18.9b0',
            'coverage==4.5.1',
            'isort==4.3.4',
            'pytest==4.4.1',
        ],
    },
    packages=setuptools.find_packages()
)
