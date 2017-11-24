#!/bin/bash

python setup.py sdist;
if [[ $BRANCH != "master" ]]
    for file in dist/*.tar.gz; do mv $file ${file//.tar.gz/$TAG.tar.gz} ; done
fi
twine upload --username $PYPI_NAME --password $PYPI_PW dist/*