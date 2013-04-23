'''CLI Entry points for handy bins'''
import yaml
import os

from docopt import docopt
from schema import Schema, Use, Or, Optional

from cfn_pyplates.options import OptionsMapping
import cfn_pyplates

def _load_pyplate(pyplate, options_mapping=None):
    'Load a pyplate file object, and return a dict of its globals'
    exec_namespace = {
        'cfn_pyplates': cfn_pyplates,
        'options_mapping': options_mapping,
    }
    exec pyplate in exec_namespace
    return exec_namespace

def _find_cloudformationtemplate(pyplate):
    '''Find a CloudFormationTemplate in a pyplate

    Goes through a pyplate namespace dict and returns the first
    CloudFormationTemplate it finds.

    '''
    for key, value in pyplate.iteritems():
        if isinstance(value, cfn_pyplates.CloudFormationTemplate):
            return value

def _open_writable(outfile_name):
    'Helper function so we can offload the opening and validation to Schema'
    return open(outfile_name, 'w')

def generate():
    '''Generate CloudFormation JSON Template based on a Pyplate

Usage:
  cfpy_generate <pyplate> [<outfile>] [-o/--options=<options_mapping>]
  cfpy_generate (-h|--help)

Arguments:
  pyplate
    Input pyplate file name

  outfile
    File in which to place the compiled JSON template
    (if omitted, outputs to stdout)

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
'''
    args = docopt(generate.__doc__)
    scheme = Schema({
        '<pyplate>': Use(open),
        '<outfile>': Or(None, '-', Use(_open_writable)),
        '--options': Or(None, Use(open)),
        '--help': Or(True, False),
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
    cft = _find_cloudformationtemplate(pyplate)

    if cft:
        outfile = args['<outfile>']
        if isinstance(outfile, file):
            outfile.write(unicode(cft))
        else:
            print(unicode(cft))
    else:
        print('No CloudFormationTemplate found in pyplate')

