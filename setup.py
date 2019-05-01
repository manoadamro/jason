# coding: utf-8

import setuptools

setuptools.setup(
    name='jason',
    version='0.1.0',
    install_requires=[
        'fire==0.1.3',
        "flask==1.0.2",
        "jsonpointer==2.0",
        "pycryptodome==3.8.1",
        "pyJWT==1.7.1",
        'waitress==1.3.0',
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
