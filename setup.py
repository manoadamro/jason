# coding: utf-8

import setuptools

setuptools.setup(
    name="jason",
    version="0.1.0",
    install_requires=[
        "fire==0.1.3",
        "flask==1.0.2",
        "jsonpointer==2.0",
        "pycryptodome==3.8.1",
        "pyJWT==1.7.1",
        "waitress==1.3.0",
    ],
    extras_require={
        "dev": [
            "behave==1.2.6",
            "black==19.3b0",
            "celery==4.3.0",
            "coverage==4.5.3",
            "docker==3.7.2",
            "flask_migrate==2.4.0",
            "flask-redis==0.3.0",
            "Flask-SQLAlchemy==2.4.0",
            "isort==4.3.4",
            "kombu==4.5.0",
            "pytest==4.4.2",
            "psycopg2-binary==2.8.2",
        ]
    },
    packages=setuptools.find_packages(),
)
