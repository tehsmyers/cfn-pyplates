# Copyright (c) 2013 ReThought Ltd
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
These utilities are ReThought additions that provide additional functionality

Useful to us, they may be quite specific in cases.
"""
import re

from cfn_pyplates.functions import join
from jinja2 import Template

# Match strings of the form {'XXX': 'YYY'} e.g.
# {'Ref': 'AWS::Region'}
FN_MATCH = re.compile("(\{\'[^\{^\}.]*\'\})")
# As above, but match only if this comprises the entire string
STRICT_MATCH = re.compile("^\{\'[^\{^\}.]*\'\}$")


def _selective_eval(s):
    """
    Takes supplied string and if it matches STRICT_MATCH, it is returned
    evaled so as to be a Python structure (dict), otherwise it is returned
    as is.

    This is to be used exclusively by templated_read to render correctly
    the CloudFormation functions that it finds in the rendered output.
    """
    if STRICT_MATCH.match(s) is None:
        return s
    return eval(s)


def templated_read(file_handle, context={}):
    """
    This function reads content from a file handle and processes as a template

    The Jinja2 templating engine is used, and the supplied context is provided.

    Once Jinja template processed, the document is split to extract
    CFN functions, e.g. Ref and Fn::Join etc, and the whole lot is
    returned Fn::Joined together (using the cfn_pyplates `join` function)

    Args:
       file_handle: any file-like object
       context: a dictionary of keys to use in the template
    """
    template = Template(file_handle.read())
    rendered = template.render(**context)
    tokens = FN_MATCH.split(rendered)

    return join("", *[_selective_eval(s) for s in tokens])
