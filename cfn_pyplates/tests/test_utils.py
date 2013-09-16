# Copyright (c) 2013 ReThought.
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
"""
Tests introduced for new utilities.
"""

import StringIO
from textwrap import dedent
import unittest2 as unittest
from cfn_pyplates.utils import (
    _selective_eval,
    templated_read,
)
from cfn_pyplates.functions import ref


class TemplatedReadTests(unittest.TestCase):
    def test_selective_eval_noeval(self):
        """
        Assert selective eval returns s if s is not a function 'atom'
        """
        s = "this is embedded {'Ref': 'AWS::StackId'} in string"
        self.assertEquals(s, _selective_eval(s))

    def test_selective_eval_evaluates(self):
        """
        Given string representing a function, evaluate
        """
        s = "{'Ref': 'AWS::StackId'}"
        expected = dict(Ref='AWS::StackId')
        self.assertEquals(expected, _selective_eval(s))

    def test_template_transform(self):
        """
        Verify that templated_read returns correct output
        """
        template = StringIO.StringIO(dedent('''\
            this is a {{ string_value }} and this is a
            {{ function_value }}'''))
        rendered = {'Fn::Join':
                    ['',
                    [u'this is a String Value and this is a\n',
                    {'Ref': 'AWS::Regions'},
                    u'']]
                    }
        context = dict(string_value="String Value",
                       function_value=ref('AWS::Regions'))

        output = templated_read(template, context)
        self.assertEquals(rendered, output)
