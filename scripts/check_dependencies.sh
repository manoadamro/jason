#!/usr/bin/env bash

sh ./scripts/list_dependencies.sh  | cut -d = -f 1 | xargs -n 1 pip3 search | grep -B2 'LATEST:'
