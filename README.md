# jason

- [Documentation](./docs)
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