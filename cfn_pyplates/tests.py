from textwrap import dedent
from tempfile import NamedTemporaryFile

import unittest2 as unittest

from cfn_pyplates.cli import generate
import cfn_pyplates

class TestResource(cfn_pyplates.BaseMapping):
    pass

class BaseMappingTestCase(unittest.TestCase):
    def test_crazy_addchild_ordering(self):
        # We should be able to add children to any element at any time,
        # before or after that element has been added to a parent.
        bm = cfn_pyplates.BaseMapping()
        tr1 = TestResource({'Id': 1})
        tr2 = TestResource({'Id': 2})
        # Tack the TestResource onto the template
        bm.add(tr1)
        # Add a child to tr1 *after* adding it to bm
        tr1.add(tr2)
        # Then make sure tr2 is visible from the template
        self.assertIn('TestResource', bm['TestResource'])
        # Double check Ids...
        self.assertEqual(bm['TestResource']['Id'], 1)
        self.assertEqual(bm['TestResource']['TestResource']['Id'], 2)

        # Now mess with the nested child, and make sure those changes
        # are still seen in the template
        tr2.update({'This Is': 'A Test'})
        self.assertEqual(bm['TestResource']['TestResource']['This Is'], 'A Test')

    def test_contructor_dict_arg(self):
        # Making sure that a resource instantiated with a params dict is updated correctly
        update_dict = {'Test': 'A custom custructydict'}
        bm = cfn_pyplates.BaseMapping()
        bm.add(TestResource(update_dict))
        self.assertEqual(bm['TestResource'], update_dict)

    def test_getsetattr(self):
        bm = cfn_pyplates.BaseMapping()

        self.assertNotIn('TestResource', bm)
        bm.test_resource = TestResource()
        self.assertIn('TestResource', bm)
        del(bm.test_resource)
        self.assertNotIn('TestResource', bm)


class CloudFormationTemplateTestCase(unittest.TestCase):
    def test_has_template_attrs(self):
        description = 'Test Description!'
        cft = cfn_pyplates.CloudFormationTemplate(description)
        self.assertEqual(cft['Description'], description)

        self.assertIn('Parameters', cft)
        self.assertIsInstance(cft.parameters, cfn_pyplates.Parameters)

        self.assertIn('Mappings', cft)
        self.assertIsInstance(cft.mappings, cfn_pyplates.Mappings)

        self.assertIn('Resources', cft)
        self.assertIsInstance(cft.resources, cfn_pyplates.Resources)

        self.assertIn('Outputs', cft)
        self.assertIsInstance(cft.outputs, cfn_pyplates.Outputs)

    def test_no_description(self):
        cft = cfn_pyplates.CloudFormationTemplate()
        self.assertNotIn('Description', cft)

    def test_jsonification(self):
        cft = cfn_pyplates.CloudFormationTemplate('This is a test')
        cft.parameters.update({'These': 'are awesome!'})

        # We expect to see the AWSTemplateFormatVersion, the provided
        # description, and the provided parameters. We do not expect to
        # see empty Mappings, Resources, or Outputs.
        expected_out = dedent(u'''\
        {
          "AWSTemplateFormatVersion": "2010-09-09",
          "Description": "This is a test",
          "Parameters": {
            "These": "are awesome!"
          }
        }''')
        self.assertEqual(unicode(cft), expected_out)

# TODO: Make the following tests work!
# Jotting down some thoughts for testing the CLI side.
# Right now, I have no idea how to call cli.generate with all the right
# arguments in sys.argv, be able to read/write stdout, etc. I'm thinking
# that patching sys with a custom argv and stdout might be the way to
# go.
#class CLITestCase(unittest.testcase):
#    def test_options_mapping(self):
#        pyplate_contents = dedent(u'''\
#        cft = CloudFormationTemplate('This is a test')
#        cft.parameters.update({
#            'Exists': options_mapping['ThisKeyExists']
#            'DoesNotExist': options_mapping['ThisKeyDoesNotExist']
#        })''')
#        options_mapping_contents = dedent(u'''\
#        {
#            'ThisKeyExists': true
#        }
#        ''')
#        pyplate = NamedTemporaryFile()
#        pyplate.write(pyplate_contents)
#        pyplate.flush()
#
#        options_mapping = NamedTemporaryFile()
#        options_mapping.write(options_mapping_contents)
#        options_mapping.flush()


if __name__ == '__main__':
    unittest.main()
