v0.0.8

- Renamed core.config to core.configuration
- Added config module for config mixins
- Added postgres config mixin with a couple of helper functions
- Added service module
- Added database module

v0.0.7
===

- Added api.token ([docs](./docs/api/token.md))

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

- Added api.schema ([docs](./docs/api/schema.md))

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
