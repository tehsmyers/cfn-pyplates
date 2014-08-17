# Copyright (c) 2013 MetaMetrics, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

'''pyplates: CloudFormation templates, generated with python

See also:

- https://aws.amazon.com/cloudformation/
- https://cfn-pyplates.readthedocs.org/ (you might already be here)
- https://github.com/seandst/cfn-pyplates/
'''

__version__ = '0.3.1'

import warnings

try:
    from semantic_version import Version

    # Validates the version above, exposes the version parts for anyone
    # that might want to make decisions based on a normalized version tuple
    version = Version(__version__)
    version_parts = tuple(version)
except ImportError:
    semver_errormsg = '''
    Failed to import semantic_version, version_parts will not be available

    This should only happen during install, before dependencies are evaluated
    and installed.
    '''
    warnings.warn(semver_errormsg, ImportWarning)

from .core import *
from .functions import *
