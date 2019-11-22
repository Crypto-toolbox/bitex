#!/usr/bin/env bash

COMMIT=$(git log --format=oneline -n 1 HEAD --format=%s)
echo ${COMMIT:0:4}