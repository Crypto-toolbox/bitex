#!/usr/bin/env bash

COMMIT=$(git log --format=oneline -n 1 HEAD --format=%s)
if [[ "${COMMIT:0:4}" == "FEAT" ]]; then
    echo minor
elif [[ "${COMMIT:0:4}" == "FIX"* ]]; then
    echo patch
else
    echo
fi