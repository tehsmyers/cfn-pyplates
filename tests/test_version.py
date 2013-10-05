from semantic_version import Version
import unittest2 as unittest

import cfn_pyplates

class TestVersionAttrs(unittest.TestCase):
    def test_version_instance(self):
        self.assertTrue(isinstance(cfn_pyplates.version, Version))

    def test_version_parts(self):
        self.assertTrue(isinstance(cfn_pyplates.version_parts, tuple))
