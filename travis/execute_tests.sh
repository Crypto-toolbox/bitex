#!/bin/bash
pip install coverage coveralls;
python setup.py install;
cd tests;
coverage run -p --source=bitex api_tests.py test;
coverage run -p --source=bitex interface_tests.py test;
coverage run -p --source=bitex pair_tests.py test;
coverage combine;
coveralls;