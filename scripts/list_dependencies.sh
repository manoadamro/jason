#!/usr/bin/env bash

python3 setup.py egg_info > /dev/null;
python3 -c "import pkg_resources ; print('\n'.join(sorted(map(str, next(pkg_resources.find_distributions('.')).requires()))))"

