from setuptools import setup
import version

setup(
    name='cfn-pyplates',
    version=version.__version__,
    author='Sean Myers',
    author_email='sean.dst@gmail.com',
    url='https://github.com/seandst/cfn-pyplates',
    packages=['cfn_pyplates', 'cfn_pyplates.version'],
    # Move the 'version' package from its position next to setup.py into
    # cfn_pyplates at install, to let setup.py and cfn_pyplates use the
    # same version source while still allowing convenience imports in
    # cfn_pyplates __init__.py that bring in potentially as-yet
    # uninstalled dependencies.
    package_dir = {
        'cfn_pyplates': 'cfn_pyplates',
        'cfn_pyplates.version': 'version',
    },
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
