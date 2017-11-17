#!/bin/bash
pip install pylint pycodestyle pydocstyle;
pylint --rcfile=pylint.rc bitex;
pycodestyle --max-line-length=100 bitex;
pydocstyle bitex;