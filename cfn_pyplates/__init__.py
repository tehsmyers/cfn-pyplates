'''pyplates: CloudFormation templates, generated with python

See also:

- https://aws.amazon.com/cloudformation/
- https://cfn-pyplates.readthedocs.org/ (you might already be here)
- https://github.com/seandst/cfn-pyplates/
'''

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
