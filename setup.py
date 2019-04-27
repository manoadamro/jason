# coding: utf-8

import setuptools


setuptools.setup(
    name='jason',
    version='0.0.13',
    install_requires=[
        "Flask==1.0.2",
        "jsonpointer==2.0",
        "PyJWT==1.7.1",
        'redis==3.2.1',
        'SQLAlchemy==1.2.18',
        'waitress==1.2.1',
    ],
    extras_require={
        'dev': [
            'black==18.9b0',
            'coverage==4.5.1',
            'fire==0.1.3',
            'isort==4.3.4',
            'pika==0.13.1',
            'pytest==4.4.1',
        ],
    },
    packages=setuptools.find_packages()
)
