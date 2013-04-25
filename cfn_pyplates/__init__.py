'''pyplates: CloudFormation templates, generated with python

The base of the package, which has convenience imports that are made available
in the global namespace of a working pyplate.
'''
# For more info, visit https://cfn-pyplates.readthedocs.org/

# Friendly PEP-386 version string
__version__ = '0.1.0'

import warnings

try:
    from verlib import NormalizedVersion
    # Validates the version above, exposing the version parts for anyone
    # that might want to make decisions based on a normalized version tuple
    version_parts = NormalizedVersion(__version__).parts
except ImportError:
    verlib_errormsg = '''
    Failed to import verlib, version_parts will not be available

    This should only happen during install, before dependencies are evaluated
    and installed.
    '''
    warnings.warn(verlib_errormsg, ImportWarning)
