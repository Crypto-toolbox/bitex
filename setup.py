from setuptools import setup, find_packages


VERSION = '2.0.0'


setup(name='BitEx', version=VERSION, author='Nils Diefenbach',
      author_email='23okrs20+pypi@mykolab.com',
      url="https://github.com/nlsdfnbch/bitex.git",
      test_suite='nose.collector', tests_require=['nose'],
      packages=find_packages(exclude=['contrib', 'docs', 'tests*', 'travis']),
      install_requires=['requests', 'pyjwt'],
      description='Python3-based API Framework for Crypto Exchanges',
      license='MIT',  classifiers=['Development Status :: 4 - Beta',
                                   'Intended Audience :: Developers'],
      )

