#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import getoutput
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


class PostInstall(install):
    pkgs = f" {requirements[-1]}"

    def run(self):
        install.run(self)
        print(getoutput('pip install' + self.pkgs))


setup(
    name='lorisapp',
    version='0.0.7',
    description='Loris',
    long_description=long_description,
    author='Matthias Christenson',
    author_email='gucky@gucky.eu',
    install_requires=requirements[:-1],
    keywords='database application',
    packages=find_packages(exclude=["docs", "images", "tests"]),
    include_package_data=True,
    scripts=['bin/lorisapp'],
    cmdclass={
        'install': PostInstall
    }
)
