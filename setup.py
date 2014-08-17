#!/usr/bin/env python

from setuptools import setup

setup(
    setup_requires=['pbr'],
    pbr=True,
    test_suite='tests',
    # Used for setup.py test, keep in sync with test-requirements.txt
    tests_require=['mock', 'unittest2'],
)
