'''Pyplates: Python-generated cloudformation templates!

Class-based representations of cloudformation templates and resources, with
the goal of baking cloudformation templates based on input config files and
pythonic classes to represent the template resource hierarchy

'''
# Friendly PEP-386 version string
__version__ = '0.0.5'

import warnings

try:
    # Get all the useful bits in this namespace explicitly
    from cfn_pyplates import exceptions
    from cfn_pyplates.base import (
        JSONableDict,
        CloudFormationTemplate,
        Parameters,
        Mappings,
        Resources,
        Outputs,
    )
    from cfn_pyplates.functions import (
        base64,
        find_in_map,
        get_att,
        get_azs,
        join,
        select,
        ref,
    )
except ImportError:
    pyplates_errormsg = '''
    Failed to import cfn_pyplates components!

    This should only happen during install, before dependencies are evaluated
    and installed.
    '''
    # Imports here can fail because dependencies aren't installed yet
    # The only time that happens is when setup.py is evaluating the
    # package version and figuring out what dependencies to install. In
    # that case, none of the handy imports above are useful.
    warnings.warn(pyplates_errormsg, ImportWarning)

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
