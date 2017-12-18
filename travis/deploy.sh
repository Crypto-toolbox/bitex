if [[$TRAVIS_TAG == ^.*rc[0-9][0-9]*$ ]]
    python generate_rc_setup.py $TRAVIS_TAG
fi
python setup.py sdist && twine upload --username $PYPI_NAME --password $PYPI_PW dist/*