# jason
---

This package was created to help me solve some of the common issues I encounter when building flask APIs.
Anyone is free to use this package in any way they see fit (as long as it conforms to the terms laid out in the licence)

As Jason is neither perfect nor complete, we welcome any contributions to help make it so.
Please refer to the [code of conduct](./CODE_OF_CONDUCT.md) and [contributing guidelines](./CONTRIBUTING.md) for more information.

*Things are likely to change (a lot) before v1.0.0*

*Jason will not support any python version below 3.7*

---

[![Version](https://img.shields.io/github/release-pre/manoadamro/Jason.svg)](https://img.shields.io/github/release-pre/manoadamro/Jason.svg)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Dependabot](https://img.shields.io/badge/Dependabot-active-brightgreen.svg)](https://img.shields.io/badge/Dependabot-active-brightgreen.svg)

|  Branch | Build  | Code Factor | Coverage  | Dependencies | 
| :-----: | :----: | :---------: | :-------: | :----------: |
| [Master](https://github.com/manoadamro/jason/tree/master)  | [![CircleCI](https://circleci.com/gh/manoadamro/jason/tree/master.svg?style=svg&circle-token=ba3677e0eb4748acd49d26bf047cf2b508fd2452)](https://circleci.com/gh/manoadamro/jason/tree/master)   | [![CodeFactor](https://www.codefactor.io/repository/github/manoadamro/jason/badge/master)](https://www.codefactor.io/repository/github/manoadamro/jason/overview/master)   | [![Coverage Status](https://coveralls.io/repos/github/manoadamro/jason/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/manoadamro/jason?branch=master)   | [![Requirements Status](https://requires.io/github/manoadamro/jason/requirements.svg?branch=master)](https://requires.io/github/manoadamro/jason/requirements/?branch=master) |
| [Develop](https://github.com/manoadamro/jason/tree/develop) | [![CircleCI](https://circleci.com/gh/manoadamro/jason/tree/develop.svg?style=svg&circle-token=ba3677e0eb4748acd49d26bf047cf2b508fd2452)](https://circleci.com/gh/manoadamro/jason/tree/develop) | [![CodeFactor](https://www.codefactor.io/repository/github/manoadamro/jason/badge/develop)](https://www.codefactor.io/repository/github/manoadamro/jason/overview/develop) | [![Coverage Status](https://coveralls.io/repos/github/manoadamro/jason/badge.svg?branch=develop&kill_cache=1)](https://coveralls.io/github/manoadamro/jason?branch=develop) | [![Requirements Status](https://requires.io/github/manoadamro/jason/requirements.svg?branch=develop)](https://requires.io/github/manoadamro/jason/requirements/?branch=develop) |


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

Definitely:
- Use green threads for the ServiceThreads extension

Probably:
- A testing package complete with mocks for everything in jason
- A module wrapping `kombu`, taking advantage of `ServiceThreads`

Maybe:
- Optional response validation (for api-testing)
- A python-docker module (for integration testing)
- A package to handle file uploads/downloads
