from setuptools import setup


setup(name='BitEx', version='2.0.0b4', author='Nils Diefenbach',
      author_email='23okrs20+pypi@mykolab.com',
      url="https://github.com/nlsdfnbch/bitex.git",
      packages=['bitex', 'bitex.api', 'bitex.api.REST', 'bitex.interface'],
      install_requires=['requests', 'pyjwt'],
      description='Python3-based API Framework for Crypto Exchanges',
      license='MIT',  classifiers=['Development Status :: 4 - Beta',
                                   'Intended Audience :: Developers'],
      )

