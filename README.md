# jason

[![CircleCI](https://circleci.com/gh/manoadamro/jason.svg?style=svg&circle-token=ba3677e0eb4748acd49d26bf047cf2b508fd2452)](https://circleci.com/gh/manoadamro/jason)

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
make check

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
- A module wrapping `celery`. `Flask-Celery` sort of thing.

Maybe:
- Optional response validation (for api-testing)
- A python-docker module (for integration testing)
- A package to handle file uploads/downloads
