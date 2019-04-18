
v0.0.2
===

- Added schema module ([docs](./docs/schema.md))

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
