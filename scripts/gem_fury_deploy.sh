#!/usr/bin/env bash

PACKAGE_DIST_PATH=$1
RESPONSE_FILE=/tmp/upload.txt

STATUS_CODE=$(curl -F package=@${PACKAGE_DIST_PATH} -w '%{http_code}' https://${GEM_FURY_PUSH_TOKEN}@push.fury.io/${GEM_FURY_USERNAME}/ -o ${RESPONSE_FILE})

tail ${RESPONSE_FILE}

if [[ ${STATUS_CODE} -ne 200 ]]; then
    echo "Unexpected HTTP response status code ${STATUS_CODE}"
    exit 1
fi
