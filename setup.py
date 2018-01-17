from distutils.core import setup


setup(name='BitEx', version='1.2.12', author='Nils Diefenbach',
      author_email='23okrs20+pypi@mykolab.com',
      url="https://github.com/nlsdfnbch/bitex.git",
      test_suite='nose.collector', tests_require=['nose'],
      packages=['bitex', 'bitex.api', 'bitex.api.WSS', 'bitex.api.REST',
                'bitex.interfaces', 'bitex.formatters'],
      install_requires=['requests', 'websocket-client', 'autobahn',
                        'pusherclient', 'nose'],
      description='Python3-based API Framework for Crypto Exchanges',
      license='MIT',  classifiers=['Development Status :: 4 - Beta',
                                   'Intended Audience :: Developers'],
      )

