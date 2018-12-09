from setuptools import setup, find_packages

VERSION = '3.0.0'


setup(
      name='BitEx',
      version=VERSION,
      author='Nils Diefenbach',
      author_email='nlsdfnbch.foss@kolabnow.com',
      url="https://github.com/nlsdfnbch/bitex.git",
      packages=find_packages(exclude=['docs', 'tests']),
      install_requires=['requests', 'pusherclient'],
      description='Python3-based API Framework for Crypto Exchanges',
      license='MIT',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers'
      ],
)
