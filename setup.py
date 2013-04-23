from setuptools import setup
from distutils.version import StrictVersion

version = '0.0.5'

# Validating the version string to prevent badness...
StrictVersion(version)

setup(
    name='cfn-pyplates',
    version=version,
    author='MetaMetrics, Inc. Systems Engineering Dept.',
    author_email='systems@lexile.com',
    packages=['cfn_pyplates'],
    install_requires=[
        'docopt',
        'ordereddict',
        'pyyaml',
        'schema',
        'unittest2',
    ],
    test_suite = 'cfn_pyplates.tests',
    entry_points={
        'console_scripts': [
            'cfn_py_generate = cfn_pyplates.cli:generate',
        ],
    },
)
