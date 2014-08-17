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

"""CLI Entry points for handy bins

Documentation for CLI methods defined in this file will be that method's
usage information as seen on the command-line.

"""
from docopt import docopt
from schema import Schema, Use, Or
import yaml

from cfn_pyplates import core, functions
from cfn_pyplates.exceptions import Error
from cfn_pyplates.options import OptionsMapping


def _load_pyplate(pyplate, options_mapping=None):
    'Load a pyplate file object, and return a dict of its globals'
    # Inject all the useful stuff into the template namespace
    exec_namespace = {
        'options': options_mapping,
    }
    for entry in core.__all__:
        exec_namespace[entry] = getattr(core, entry)
    for entry in functions.__all__:
        exec_namespace[entry] = getattr(functions, entry)

    # Do the needful.
    exec pyplate in exec_namespace
    return exec_namespace


def _find_cloudformationtemplate(pyplate):
    """Find a CloudFormationTemplate in a pyplate

    Goes through a pyplate namespace dict and returns the first
    CloudFormationTemplate it finds.

    """
    for key, value in pyplate.iteritems():
        if isinstance(value, core.CloudFormationTemplate):
            return value

    # If we haven't returned something, it's an Error
    raise Error('No CloudFormationTemplate found in pyplate')


def _open_writable(outfile_name):
    'Helper function so we can offload the opening and validation to Schema'
    return open(outfile_name, 'w')


def generate():
    """Generate CloudFormation JSON Template based on a Pyplate

Usage:
  cfn_py_generate <pyplate> [<outfile>] [-o/--options=<options_mapping>]
  cfn_py_generate (-h|--help)
  cfn_py_generate --version

Arguments:
  pyplate
    Input pyplate file name

  outfile
    File in which to place the compiled JSON template
    (if omitted or '-', outputs to stdout)

Options:
  -o --options=<options_mapping>
    Input JSON or YAML file for options mapping
    exposed in the pyplate as "options_mapping"

  -h --help
    This usage information

WARNING!
  Do not use pyplates that you haven't personally examined!

  A pyplate is a crazy hybrid of JSON-looking python.
  exec is used to read the pyplate, so any code in there is going to
  run, even potentailly harmful things.

  Be careful.
"""
    from pkg_resources import require
    version = require("cfn-pyplates")[0].version
    args = docopt(generate.__doc__, version=version)
    scheme = Schema({
        '<pyplate>': Use(open),
        '<outfile>': Or(None, '-', Use(_open_writable)),
        '--options': Or(None, Use(open)),
        '--help': Or(True, False),
        '--version': Or(True, False),
    })
    args = scheme.validate(args)

    options_file = args['--options']
    if options_file:
        options = yaml.load(options_file)
    else:
        options = {}

    options_mapping = OptionsMapping(options)

    # Not sure if Scheme can validate one options based on the value of
    # another, but some pyplates need options_mapping to load and some
    # don't. We could validate the second case easily enough, but in the
    # first case we'd have to pass the options mapping in to the test
    # function. Not sure that's possible.
    pyplate = _load_pyplate(args['<pyplate>'], options_mapping)

    try:
        cft = _find_cloudformationtemplate(pyplate)
        output = unicode(cft)
    except Error as e:
        print 'Error processing the pyplate:'
        print e.message
        return 1

    outfile = args['<outfile>']
    if isinstance(outfile, file):
        outfile.write(output)
    else:
        print(output)

    # Explicitly return a posixy "EVERYTHING IS OKAY" 0
    return 0
