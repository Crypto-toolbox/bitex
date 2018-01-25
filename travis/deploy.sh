if [ "$TRAVIS_TAG" =~ ^.*rc[0-9][0-9]*$ ]; then
    echo "ReleaseCandidate Tag found, running RC setup.."
    python $TRAVIS_BUILD_DIR/travis/generate_rc_setup.py $TRAVIS_TAG && echo "done!"
elif [ "$TRAVIS_BRANCH" = "nightly" ]; then
    echo "Branch is nightly, running nightly setup.."
    python $TRAVIS_BUILD_DIR/travis/generate_nightly_setup.py && echo "done!"
fi
echo "Building source distribution.."
python setup.py sdist

if [ $? -eq 1 ]; then
    echo "Build complete. Initializing upload via twine.."
    twine upload --username $PYPI_NAME --password $PYPI_PW dist/* && echo "Upload successful!" || echo "Upload failed!"
else
    echo "Building source distribution failed. Skipping upload."
fi

echo "Deploy script complete."