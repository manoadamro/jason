#!/usr/bin/env bash

echo "checking dependencies..."

IFS=$'\n' read -rd '' -a OUTDATED <<<"$(pip list --outdated | awk "NR>2")"
COUNT=${#OUTDATED[@]}

for each in "${OUTDATED[@]}"
do
  echo "$each"
done
echo "number of outdated dependencies: ${COUNT}"

if [[ "$COUNT" -ne "0" ]]; then
  exit ${COUNT}
fi
