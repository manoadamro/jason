#!/usr/bin/env bash

for i in `seq 1 ${3}`;
do
  nc -z ${1} ${2} && exit 0
  echo -n .
  sleep 1
done
echo "Failed waiting for ${1}:${2} after ${3} seconds" && exit 1
