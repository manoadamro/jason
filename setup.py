# coding: utf-8

import setuptools

setuptools.setup(
    name="jason",
    version="0.1.2",
    install_requires=[
        "fire==0.1.3",
        "flask==1.1.1",
        "jsonpointer==2.0",
        "pycryptodome==3.8.2",
        "pyJWT==1.7.1",
        "waitress==1.3.0",
    ],
    extras_require={
        "dev": [
            "behave==1.2.6",
            "black==19.3b0",
            "celery==4.3.0",
            "coverage==4.5.3",
            "docker==4.0.2",
            "flask_migrate==2.5.2",
            "flask-redis==0.4.0",
            "Flask-SQLAlchemy==2.4.0",
            "isort==4.3.21",
            "kombu==4.6.3",
            "pytest==5.0.1",
            "psycopg2-binary==2.8.3",
        ]
    },
    packages=setuptools.find_packages(),
)
