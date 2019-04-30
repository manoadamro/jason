#!/usr/bin/env bash

python3 -c "import pkg_resources ; print('\n'.join(sorted(map(str, next(pkg_resources.find_distributions('.')).requires()))))" | cut -d = -f 1 | xargs -n 1 pip3 search | grep -B2 'LATEST:';
