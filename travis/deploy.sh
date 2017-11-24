#!/bin/bash

python setup.py sdist;
for file in dist/*.tar.gz; do mv $file ${file//.tar.gz/$TAG.tar.gz} ; done;
twine upload --username $PYPI_NAME --password $PYPI_PW dist/*;