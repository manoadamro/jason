# jason

- [Documentation](./docs/jason.md)
- [Examples](./examples)
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
- Create an `ext` package and sub-class each extension (flask_sqlalchemy, flask_redis, celery),
override the init_app method and use `some_extension.init_app(app)` instead of `app.init_some_extension(extension)`
- Use green threads for the AppThreads extension

Probably:
- A testing package complete with mocks for everything in jason
- A module wrapping `kombu`, taking advantage of `AppThreads`
- A module wrapping `celery`. `Flask-Celery` sort of thing.

Maybe:
- Optional response validation (for api-testing)
- A python-docker module (for integration testing)
- A package to handle file uploads/downloads
