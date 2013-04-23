'''Python wrappers for CloudFormation functions

They don't do much more than clean up the pyplates, so that they look a
little more like python than JSON

Notes:
* To avoid the issue of using the wrong types with functions that take
  sequences as input (join, select), argument unpacking is used. Therefore,
  pass the sequence elements one at a time, rather than the sequence itself,
  after passing the separator (for join) or index (for select).
* Using CloudFormation's Join function versus a pythonic 'sep'.join will
  avoid any issues that could arise when the string join method coerces its
  arguments to strings.
* FindInMap and Select are represented in here "just in case". Most
  likely, using the python equivalent in a pyplate will be easier to
  look at and maintain.
Current list of Amazon functions:
http://docs.amazonwebservices.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html

'''

def base64(value):
    return {'Fn::Base64': value}

def find_in_map(map_name, key, value):
    return {'Fn::FindInMap': [map_name, key, value]}

def get_att(logical_name, attribute):
    return {'Fn::GetAtt': [logical_name, attribute]}

def get_azs(region=''):
    return {'Fn::GetAZs': region}

def join(sep, *args):
    return {'Fn::Join': [sep, list(args)]}

def select(index, *args):
    return {'Fn::Select': [index, list(args)]}

def ref(logical_name):
    return {'Ref': logical_name}

