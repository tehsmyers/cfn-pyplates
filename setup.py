from setuptools import setup

import cfn_pyplates

setup(
    name='cfn-pyplates',
    version=cfn_pyplates.__version__,
    author='Sean Myers',
    author_email='sean.dst@gmail.com',
    url='https://github.com/seandst/cfn-pyplates',
    packages=['cfn_pyplates'],
    description='Amazon Web Services CloudFormation template generator',
    long_description=open('README.rst').read(),
    install_requires=[
        'distribute',
        'docopt',
        'ordereddict',
        'pyyaml',
        'schema',
        'unittest2',
        'verlib',
    ],
    test_suite = 'cfn_pyplates.tests',
    tests_require = ['mock'],
    entry_points={
        'console_scripts': [
            'cfn_py_generate = cfn_pyplates.cli:generate',
        ],
    },
    license='LICENSE',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
)
