#!/usr/bin/env python

from setuptools import setup
import os
import sys

min_py_version = (3, 7)

if sys.version_info < min_py_version:
    sys.exit(
        'Loris is only supported '
        'on Python {}.{} or higher'.format(*min_py_version))

path = os.path.abspath(os.path.dirname(__file__))

long_description = 'Data management and analysis application for DataJoint'

with open(os.path.join(path, 'requirements.txt')) as f:
    requirements = f.read().split()


setup(name='loris',
      version='0.1',
      description='Loris',
      long_description=long_description,
      author='Matthias Christenson',
      author_email='gucky@gucky.eu',
      install_requires=requirements,
      keywords='database application', 
      packages=['loris']
)
