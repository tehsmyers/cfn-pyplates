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

import unittest2 as unittest

from cfn_pyplates import exceptions, functions


class IntrinsicFuncsTestCase(unittest.TestCase):
    def test_base64(self):
        ret = functions.base64('test')
        self.assertEqual(ret['Fn::Base64'], 'test')

    def test_find_in_map(self):
        ret = functions.find_in_map('MapName', 'MapKey', 'MapValue')
        self.assertEqual(ret['Fn::FindInMap'], ['MapName', 'MapKey', 'MapValue'])

    def test_get_att(self):
        ret = functions.get_att('ThingName', 'AttrName')
        self.assertEqual(ret['Fn::GetAtt'], ['ThingName', 'AttrName'])

    def test_get_azs(self):
        ret = functions.get_azs('region')
        self.assertEqual(ret['Fn::GetAZs'], 'region')

    def test_join(self):
        ret = functions.join('.', 'x', 'y', 'z')
        self.assertEqual(ret['Fn::Join'], ['.', ['x', 'y', 'z']])

    def test_select(self):
        ret = functions.select(3, 1, 2, 3, 4, 5)
        self.assertEqual(ret['Fn::Select'], [3, [1, 2, 3, 4, 5]])

    def test_ref(self):
        ret = functions.ref('ThingName')
        self.assertEqual(ret['Ref'], 'ThingName')

    def test_and(self):
        ret = functions.c_and('Thing 1', 'Thing 2')
        self.assertEqual(ret['Fn::And'], ['Thing 1', 'Thing 2'])

    def test_or(self):
        ret = functions.c_or('Thing 1', 'Thing 2')
        self.assertEqual(ret['Fn::Or'], ['Thing 1', 'Thing 2'])

    def test_not(self):
        ret = functions.c_not('Thing')
        self.assertEqual(ret['Fn::Not'], ['Thing'])

    def test_if(self):
        ret = functions.c_if('If', "Condition 1", "Condition 2")
        self.assertEqual(ret['Fn::If'], ['If', 'Condition 1', 'Condition 2'])

    def test_equals(self):
        ret = functions.c_equals('Thing 1', 'Thing 2')
        self.assertEqual(ret['Fn::Equals'], ['Thing 1', 'Thing 2'])


class IntrinsicFuncsFailureCase(unittest.TestCase):
    def test_join_unjoinable(self):
        with self.assertRaises(exceptions.IntrinsicFuncInputError) as ctx:
            functions.join('.')
        self.assertEqual(ctx.exception.message,
            functions.join._errmsg_needinput)

        with self.assertRaises(exceptions.IntrinsicFuncInputError) as ctx:
            functions.join('.', 'x')
        self.assertEqual(ctx.exception.message,
            functions.join._errmsg_needinput)

    def test_select_int(self):
        with self.assertRaises(exceptions.IntrinsicFuncInputError) as ctx:
            functions.select('not an int')
        self.assertEqual(ctx.exception.message,
            functions.select._errmsg_int)

    def test_select_empty(self):
        with self.assertRaises(exceptions.IntrinsicFuncInputError) as ctx:
            functions.select(0)
        self.assertEqual(ctx.exception.message,
            functions.select._errmsg_empty)

    def test_select_null(self):
        with self.assertRaises(exceptions.IntrinsicFuncInputError) as ctx:
            functions.select(0, '', None)
        self.assertEqual(ctx.exception.message,
            functions.select._errmsg_null)

    def test_select_index(self):
        with self.assertRaises(exceptions.IntrinsicFuncInputError) as ctx:
            functions.select(2, '', '')
        self.assertEqual(ctx.exception.message,
            functions.select._errmsg_index)

    def test_and_min(self):
        with self.assertRaises(exceptions.IntrinsicFuncInputError) as ctx:
            functions.c_and('1 Condition')
        self.assertEqual(ctx.exception.message,
            functions.c_and._errmsg_min)

    def test_and_max(self):
        with self.assertRaises(exceptions.IntrinsicFuncInputError) as ctx:
            functions.c_and(*['%d Condition' % i for i in range(20)])
        self.assertEqual(ctx.exception.message,
            functions.c_and._errmsg_max)

    def test_or_min(self):
        with self.assertRaises(exceptions.IntrinsicFuncInputError) as ctx:
            functions.c_or('1 Condition')
        self.assertEqual(ctx.exception.message,
            functions.c_or._errmsg_min)

    def test_or_max(self):
        with self.assertRaises(exceptions.IntrinsicFuncInputError) as ctx:
            functions.c_or(*['%d Condition' % i for i in range(20)])
        self.assertEqual(ctx.exception.message,
            functions.c_or._errmsg_max)
