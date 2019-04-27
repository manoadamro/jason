v0.0.14
===

- Added crypto module ([docs](./docs/crypto.md))

v0.0.13
===

- Schema validation will process everything, 
collect the errors and raise at the end now rather than raising as soon as it hits an error
- Added some basic logging

v0.0.12
===

- Removed core and api packages and flattened everything


v0.0.11
===

- Added basic cache module ([docs](./docs/cache.md))

v0.0.11
===

- Moved cli methods to class

v0.0.10
===

- Updated cli 
- service module is now a package
- Removed config mixin package and made service types and plugins responsible for their own config mixins

v0.0.9
===

- Added basic cli for running services ([docs](./docs/cli.md))

v0.0.8
===

- Added service module ([docs](./docs/service.md))
- Added database module ([docs](./docs/database.md))
- Added config module for config mixins
- Added flask config mixin
- Added rabbit config mixin
- Added postgres config mixin
- Renamed core.config to core.configuration

v0.0.7
===

- Added api.token ([docs](docs/token.md))

v0.0.6
===

- CircleCi integration
- improved setup.py
    - added extra requires (dev) and pytest requirement
- added `install-dev` to makefile

    
v0.0.5
===

- created core namespace
    - moved config to jason.core
    - moved schema to jason.core
    - moved utils to jason.core

v0.0.4
===

- Added api.schema ([docs](./docs/schema.md))

v0.0.3
===

- Added config module ([docs](docs/core/configuration.md))

- Added `check` to makefile
- Added basic instructions to `README.md`

v0.0.2
===

- Added schema module ([docs](docs/core/schema.md))

v0.0.1
===

- Added setup.py
- Added empty README.md
- Added README.md (this file)
- Added RELEASES.md (this file)
- added Makefile
    - install: upgrades pip and force-reinstall jason
    - cloc: runs [cloc](https://github.com/AlDanial/cloc) on the source code 
    - format: formats code with isort and black
    - test:  runs tests with pytest and checks with isort and black
    - pre-commit: runs format followed by test
- Added .coveragerc with basic coverage settings
- Added .isort.cfg with basic isort settings
- Added .gitignore with standard python configuration
