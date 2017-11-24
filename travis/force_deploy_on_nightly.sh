#!/bin/bash

if [[$TRAVIS_BRANCH == "nightly" ]]
    python setup.py sdist
    twine upload --username $PYPI_NAME --password $PYPI_PW dist/*
fi