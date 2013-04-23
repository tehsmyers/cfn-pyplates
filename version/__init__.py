# Friendly version string, see PEP-386
# This is the one you edit
__version__ = '0.0.5'

from verlib import NormalizedVersion
# Validates the version above, and exposes the version parts for anyone
# that might want to make decisions based on ints in version tuples
version_parts = NormalizedVersion(__version__).parts
