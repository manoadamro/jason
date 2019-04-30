#!/usr/bin/env bash
set -e

python3 -c "import pkg_resources ; print('\n'.join(sorted(map(str, next(pkg_resources.find_distributions('.')).requires()))))"
