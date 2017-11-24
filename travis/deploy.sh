if [[$TRAVIS_BRANCH == release* ]]
    python generate_rc_setup.py $TRAVIS_TAG
fi
python setup.py sdist && twine upload --username $PYPI_NAME --password $PYPI_PW dist/*