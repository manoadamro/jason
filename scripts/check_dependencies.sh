#!/usr/bin/env bash
set -e

sh ./scripts/list_dependencies.sh  | cut -d = -f 1 | xargs -n 1 pip3 search | grep -B2 'LATEST:';
