#!/usr/bin/env python

from setuptools import setup, find_packages
import os

ZTHREADS_CYTHON = os.getenv("ZTHREADS_CYTHON", None)


if ZTHREADS_CYTHON:
    from Cython.Build import cythonize
    cythonkw = {
        "ext_modules": cythonize(
            ["zthreads/threadpools/threadpools.py",
             "zthreads/comm/fileoperation.py",
             "zthreads/comm/logger.py",
             ])
    }
else:
    cythonkw = {}
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''


setup(
    name='zthreads',
    version='1.00',
    description='A Python Interface to TDX protocol',
    long_description=long_description,
    author='allisnone',
    author_email='i@allisnone.cc',
    url='https://github.com/allisnone/zthreads',
    packages=find_packages(),
    install_requires=[
            'paramiko',
            #'shutil',
            #'hashlib',
    ],
    entry_points={
          'console_scripts': [
              'test=threadpools_test:main',
          ]
      },
    **cythonkw
    )

