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

from cStringIO import StringIO
from textwrap import dedent
from tempfile import NamedTemporaryFile
import json
import sys
import unittest

from cfn_pyplates import cli

try:
    from mock import patch
    mock_error = None
except ImportError:
    patch = None
    mock_error = 'skipped -- install mock to run this test'


@unittest.skipIf(patch is None, mock_error)
class CLITestCase(unittest.TestCase):
    def setUp(self):  # NOQA
        # Patch out argv, stdin, and stdout so that we can do some
        # useful things, like:
        # - Fake arguments to be used by a CLI function
        # - Write to stding, simulating user input
        # - Suppress stdout to hide prompts during the test run
        argv_patcher = patch('sys.argv')
        argv_patcher.start()
        self.addCleanup(argv_patcher.stop)
        stdin_patcher = patch('sys.stdin', new=StringIO())
        stdin_patcher.start()
        self.addCleanup(stdin_patcher.stop)
        stdout_patcher = patch('sys.stdout', new=StringIO())
        stdout_patcher.start()
        self.addCleanup(stdout_patcher.stop)

    def _make_pyplate(self, contents):
        contents = dedent(contents)
        pyplate = NamedTemporaryFile()
        pyplate.write(contents)
        pyplate.flush()
        return pyplate

    def _generate(self, fail_on_error=True):
        return_code = cli.generate()
        sys.stdout.seek(0)
        out = '\n'.join([line for line in sys.stdout.readlines()])
        if return_code != 0:
            if fail_on_error:
                self.fail('generate failed, stdout dump follows:\n{0}'.format(
                    out)
                )
        return out

    def test_generate(self):
        # Make a pyplate that uses the options mapping
        pyplate = self._make_pyplate(u'''\
        cft = CloudFormationTemplate('This is a test')
        cft.parameters.update({
            'Exists': options['ThisKeyExists'],
            'DoesNotExist': options['ThisKeyDoesNotExist']
        })''')

        # Now make an options mapping with only one of those keys in it
        # to simultaneously test options interpolation and
        # user-prompted input
        options_mapping_contents = dedent(u'''\
        {
            'ThisKeyExists': true
        }
        ''')
        options_mapping = NamedTemporaryFile()
        options_mapping.write(options_mapping_contents)
        options_mapping.flush()

        # The outfile which will receive the rendered json
        outfile = NamedTemporaryFile()

        # Populate sys.argv with something reasonable based on all the
        # tempfiles. On the command line this would look like
        # "cfn_py_generate pyplate outfile -o options_mapping"
        sys.argv = ['cfn_py_generate', pyplate.name, outfile.name,
            '-o', options_mapping.name]
        # Prime stdin with the answer to our interactive question
        input = 'Test'
        sys.stdin.write('{0}\n'.format(input))
        sys.stdin.seek(0)

        # Run the command, catch it if it tries to exit the interpreter
        self._generate()

        # Load the template back into python for assertions
        template = json.load(outfile)

        # The Exists parameter should evaluate to bool True...
        # If so, then options_mapping interpolation works
        self.assertTrue(template['Parameters']['Exists'])

        # The DoesNotExist parameter should be what was injected to stdin
        # If so, then prompts to populate missing options_mapping entries work
        self.assertEqual(template['Parameters']['DoesNotExist'], input)

    def test_generate_no_options_no_outfile(self):
        # generate with no options mapping to stdout
        description = 'This is a test.'
        pyplate = self._make_pyplate("cft = CloudFormationTemplate('{}')".format(description))

        # Populate sys.argv with something reasonable based on all the
        # tempfiles. On the command line this would look like
        # "cfn_py_generate pyplate outfile -o options_mapping"
        sys.argv = ['cfn_py_generate', pyplate.name, '-']

        template = json.loads(self._generate())

        # The description in the template should match the one in the pyplate
        self.assertEqual(template['Description'], description)

    def test_generate_stdin_options(self):
        # Make a pyplate that uses the options mapping
        pyplate = self._make_pyplate(u'''\
        cft = CloudFormationTemplate('This is a test')
        cft.parameters.update({
            'Exists': options['ThisKeyExists'],
        })''')

        # Prime stdin with the contents of the options file
        sys.stdin.write('{0}\n'.format(dedent(u'''\
        {
            'ThisKeyExists': true
        }
        ''')))
        sys.stdin.seek(0)

        # Populate sys.argv with something reasonable based on all the
        # tempfiles. On the command line this would look like
        # "cfn_py_generate pyplate outfile -o options_mapping"
        sys.argv = ['cfn_py_generate', pyplate.name, '-o', '-']

        template = json.loads(self._generate())

        # The Exists parameter should evaluate to bool True...
        # If so, then options_mapping interpolation works
        self.assertTrue(template['Parameters']['Exists'])

    def test_broken_pyplate(self):
        pyplate = self._make_pyplate(u'''\
        I am a broken pyplate.
        })''')
        sys.argv = ['cfn_py_generate', pyplate.name]
        out = self._generate(fail_on_error=False)
        # This pyplate should fail because its python syntax isn't valid
        self.assertIn('SyntaxError', out)
