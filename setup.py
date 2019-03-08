#!/usr/bin/env python3.6
# coding: utf-8
import codecs
import os
import sys
from __init__ import VERSION

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist')
    os.system('twine upload dist/*')
    sys.exit()

with codecs.open('README.rst') as file:
    long_description = file.read()
    if not isinstance(long_description, str):
        long_description = str(long_description, 'utf-8')


setup(
    name='TileEngine',
    version=VERSION,
    description='Basic 2D tile-based game engine, based on Pokemon.',
    long_description=long_description,
    author='WORD559',
    author_email='josh.barrass.work@gmail.com',
    url='https://github.com/WORD559/TileEngine',
    scripts=[],
    packages=['TileEngine'],
    package_dir={
        'TileEngine': '.',
        },
    install_requires=['Pillow'],
    keywords='game engine tile pokemon',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ]
)
