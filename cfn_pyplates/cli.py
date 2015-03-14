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
import sys

import yaml
from docopt import docopt
from schema import Schema, Use, Or

from cfn_pyplates import core
from cfn_pyplates.options import OptionsMapping


def _open_outfile(outfile_name):
    'Helper function for Schema to open the outfile'
    if outfile_name == '-':
        return sys.stdout
    else:
        return open(outfile_name, 'w')


def _open_optionfile(optionfile_name):
    'Helper function for Schema to open the option file'
    if optionfile_name == '-':
        return sys.stdin
    else:
        return open(optionfile_name)


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
    (if '-', accepts input from stdin)

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
        '<outfile>': Or(None, Use(_open_outfile)),
        '--options': Or(None, Use(_open_optionfile)),
        '--help': Or(True, False),
        '--version': Or(True, False),
    })
    args = scheme.validate(args)

    options_file = args['--options']
    if options_file:
        options = yaml.load(options_file)
    else:
        options = {}

    output = core.generate_pyplate(args['<pyplate>'], OptionsMapping(options))

    if not output:
        return 1

    if not args['<outfile>'] or args['<outfile>'] == '-':
        print output
    else:
        args['<outfile>'].write(output)

    # Explicitly return a posixy "EVERYTHING IS OKAY" 0
    return 0
