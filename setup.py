# coding: utf-8

import setuptools


setuptools.setup(
    name='jason',
    version='0.0.9',
    install_requires=[
        "Flask==1.0.2",
        "PyJWT==1.7.1",
        "jsonpointer==2.0",
        'waitress==1.2.1',
        'SQLAlchemy==1.2.18'
    ],
    extras_require={
        'dev': [
            'pytest==4.4.1',
            'isort==4.3.4',
            'black==18.9b0',
            'coverage==4.5.1',
            'pika==0.13.1',
            'fire==0.1.3'
        ]
    },
    packages=setuptools.find_packages()
)
