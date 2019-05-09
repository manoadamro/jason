# jason

[![Version](https://img.shields.io/github/release-pre/manoadamro/Jason.svg)](https://img.shields.io/github/release-pre/manoadamro/Jason.svg)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) 
[![CodeFactor](https://www.codefactor.io/repository/github/manoadamro/jason/badge)](https://www.codefactor.io/repository/github/manoadamro/jason)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

---

| Master | Develop |
| :----: | :-----: |
| [![CircleCI](https://circleci.com/gh/manoadamro/jason/tree/master.svg?style=svg&circle-token=ba3677e0eb4748acd49d26bf047cf2b508fd2452)](https://circleci.com/gh/manoadamro/jason/tree/master) | [![CircleCI](https://circleci.com/gh/manoadamro/jason/tree/develop.svg?style=svg&circle-token=ba3677e0eb4748acd49d26bf047cf2b508fd2452)](https://circleci.com/gh/manoadamro/jason/tree/develop) |
| [![Coverage Status](https://coveralls.io/repos/github/manoadamro/jason/badge.svg?branch=master)](https://coveralls.io/github/manoadamro/jason?branch=master) | [![Coverage Status](https://coveralls.io/repos/github/manoadamro/jason/badge.svg?branch=develop)](https://coveralls.io/github/manoadamro/jason?branch=develop)


- [Documentation](./docs/jason.md)
- [Examples](./examples)
    - [Basic](examples/basic_example.py)
    - [JWT](examples/jwt_example.py)
    - [Consumer](examples/consumer_example.py)
    - [Celery](examples/celery_example.py)
- [Release Notes](./RELEASES.md)

### Installation

To install jason and its dependencies, simply run:

```bash
make install

```

or to install test dependencies as well:

```bash
make install-dev

```

### Running Tests:

To run unit tests and doc tests, run:

```bash
make test

```

To check code formatting:

```bash
make lint

```

To run code formatter:

```bash
make format

```

### Committing Code

Before committing code, run the following:

```bash
make pre-commit

```

this will run the formatter, unit tests and doc tests.


### The Future of Jason

This is a start, but there is a lot left to do...

Definitely:
- Use green threads for the ServiceThreads extension

Probably:
- A testing package complete with mocks for everything in jason
- A module wrapping `kombu`, taking advantage of `ServiceThreads`

Maybe:
- Optional response validation (for api-testing)
- A python-docker module (for integration testing)
- A package to handle file uploads/downloads
