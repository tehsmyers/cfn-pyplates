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

"""Python wrappers for CloudFormation intrinsic functions

These are all available without preamble in a pyplate's global namespace.

These help make the pyplate look a little more like python than JSON, and can
be ignored if you want to write the raw JSON directly. (But you don't want
that, right? After all, that's why you're using pyplates.)

Notes:

* All "Return" values are a little midleading, in that what really gets
  returned is the JSON-ified CFN intrinsic function. When using these in
  pyplates, though, it's probably easiest to forget that and only be
  concerned with how CFN will handle this, hence the Return values.
* To avoid the issue of using the wrong types with functions that take
  sequences as input (join, select), argument unpacking is used. Therefore,
  pass the sequence elements one at a time, rather than the sequence itself,
  after passing the separator (for join) or index (for select).
* Using CloudFormation's Join function versus a pythonic 'string'.join
  allows you to use CFN's intrinsic functions inside a join statement. The
  pythonic string join method may literally interpret a call to an intrinsic
  function, causing the resulting JSON to be interpreted as a string and
  ignored by the CloudFormation template parser
* Functions related to conditions tend to overlap with python keywords, so they
  are prefixed with ``c_`` to differentiate them (so, Fn::And become ``c_and``)

.. note:
    Documentation for the functions is verbatim from the AWS Docs,
    except where identifiers are changed to fit with normal python style.

    Links:
    * `Intrinsic Functions <cfn-functions_>`_
    * `Intrinsic Condition Functions <cfn-functions-conditions_>`_


"""

# Where needed, exception error messages are stored on the intrinsic function
# wrappers to make testing the function failure cases very easy


from exceptions import IntrinsicFuncInputError

__all__ = [
    'base64',
    'find_in_map',
    'get_att',
    'get_azs',
    'join',
    'select',
    'ref',
    'c_ref',
    'c_and',
    'c_or',
    'c_not',
    'c_if',
    'c_equals',
]


def base64(value):
    """The intrinsic function Fn::Base64 returns the Base64 representation of \
    the input string.

    This function is typically used to pass encoded data to
    Amazon EC2 instances by way of the UserData property.

    Args:
        value: The string value you want to convert to Base64

    Returns: The original string, in Base64 representation
    """
    return {'Fn::Base64': value}


def find_in_map(map_name, key, value):
    """The intrinsic function Fn::FindInMap returns the value of a key from a \
    mapping declared in the Mappings section.

    Args:
        map_name: The logical name of the mapping declared in the Mappings
            section that contains the key-value pair.
        key: The name of the mapping key whose value you want.
        value: The value for the named mapping key.

    Returns: The map value.

    .. note:
        find_in_map is represented here "just in case".
        Most likely, using the python equivalent in a pyplate will be
        easier to both look at and maintain.

    """
    return {'Fn::FindInMap': [map_name, key, value]}


def get_att(logical_name, attribute):
    """The intrinsic function Fn:GetAtt returns the value of an attribute from \
    a resource in the template.

    Args:
        logical_name: The logical name of the resource that
            contains the attribute you want.
        attribute: The name of the resource-specific attribute
            whose value you want. See the resource's reference




 page
            [#cfn-resources] for details about the attributes available
            for that resource type.

    Returns: The attribute value.

    """
    return {'Fn::GetAtt': [logical_name, attribute]}


def get_azs(region=''):
    """The intrinsic function Fn::GetAZs returns an array that lists all \
    Availability Zones for the specified region.

    Because customers have access to different Availability Zones, the
    intrinsic function Fn::GetAZs enables template authors to write
    templates that adapt to the calling user's access. This frees you from
    having to hard-code a full list of Availability Zones for a specified
    region.

    Args:
        region: The name of the region for which you want to get the
            Availability Zones.
            You can use the AWS::Region pseudo parameter to specify the region
            in which the stack is created. Specifying an empty string is
            equivalent to specifying AWS::Region.
    Returns: The list of Availability Zones for the region.

    """
    return {'Fn::GetAZs': region}


def join(sep, *args):
    """The intrinsic function Fn::Join appends a set of values into a single \
    value, separated by the specified delimiter.

    If a delimiter is the empty string, the set of values are
    concatenated with no delimiter.

    Args:
        delimiter: The value you want to occur between fragments. The delimiter
            will occur between fragments only.
            It will not terminate the final value.

        *args: Any number of values you want combined, passed as
            positional arguments

    Returns: The combined string.

    """
    if len(args) < 2:
        raise IntrinsicFuncInputError(join._errmsg_needinput)

    return {'Fn::Join': [sep, list(args)]}

join._errmsg_needinput = 'Unable to join on one or less things!'


def select(index, *args):
    """The intrinsic function Fn::Select returns a single object from a list of objects by index.

    .. note:
        select is represented here "just in case".
        Most likely, using the python equivalent in a pyplate will be
        easier to both look at and maintain, but in the event that selects
        need to take place after CFN has interpolated all the intrinsic
        functions, it may still be useful.

    .. warning:: Important
        Fn::Select does not check for null values or if the index is out of
        bounds of the array. Both conditions will result in a stack error,
        so you should be certain that the index you choose is valid, and that
        the list contains non-null values.

    Args:
        index: The index of the object to retrieve. This must be a value
            from zero to N-1, where N represents the number of
            elements in the array.
        *args: Any number of objects to select from, passed as
            positional arguments. None of the arguments can be ``None``

    Returns: The selected object.

    """
    try:
        index = int(index)
    except ValueError:
        raise IntrinsicFuncInputError(select._errmsg_int)
    if not args:
        raise IntrinsicFuncInputError(select._errmsg_empty)
    if filter(lambda x: x is None, args):
        raise IntrinsicFuncInputError(select._errmsg_null)
    try:
        args[index]
    except IndexError:
        raise IntrinsicFuncInputError(select._errmsg_index)

    return {'Fn::Select': [index, list(args)]}

select._errmsg_int = 'Index must be a number!'
select._errmsg_empty = 'Unable to select from an empty list!'
select._errmsg_null = 'List of selections include null values!'
select._errmsg_index = 'Provided index is invalid!'


def ref(logical_name):
    """The intrinsic function Ref returns the value of the specified parameter or resource.

    When you are declaring a resource in a template and you need to
    specify another template resource by name, you can use the Ref to refer
    to that other resource. In general, Ref returns the name of the
    resource. For example, a reference to an
    AWS::AutoScaling::AutoScalingGroup returns the name of that Auto
    Scaling group resource.

    For some resources, an identifier is returned that has another
    significant meaning in the context of the resource. An AWS::EC2::EIP
    resource, for instance, returns the IP address, and an
    AWS::EC2::Instance returns the instance ID.

    Args:
        logical_name: The logical name of the resource or parameter you want
            to dereference.

    Returns:
        * When you specify a parameter's logical name, it returns the value
            of the parameter.
        * When you specify a resource's logical name, it returns a value
            that you can typically use to refer to that resource.

    .. note:: You can also use Ref to add values to Output messages.

    """
    return {'Ref': logical_name}


def c_ref(condition_name):
    """The intrinsic function Condition used to reference a named condition

    When you refer to a condition in another condition or associate the
    condition with a resource, you use the Condition: key. For the Fn::If
    function, you only need to specify the condition name.

    Args:
        condition_name: The name of the condition you want to reference.

    Returns:
        * A reference to the named condition

    """
    return {'Condition': condition_name}


def _validate_logical_condition_counts(fn, conditions):
    # c_and / c_or have these limits applied, this keeps it DRY
    if len(conditions) < 2:
        raise IntrinsicFuncInputError(fn._errmsg_min)
    elif len(conditions) > 10:
        raise IntrinsicFuncInputError(fn._errmsg_max)


def c_and(*conditions):
    """The intrinsic conditional function Fn::And

    Returns true (for the pruposes of the cfn template) if all the specified conditions
    evaluate to true, or returns false if any one of the conditions evaluates to false.

    Fn::And acts as an AND operator.

    The minimum number of conditions that you can include is 2, and the maximum is 10.

    Args:
        *conditions: The conditions to evaluate

    """
    _validate_logical_condition_counts(c_and, conditions)
    return {'Fn::And': list(conditions)}
c_and._errmsg_min = "Minimum umber of conditions for 'c_and' condition is 2"
c_and._errmsg_max = "Maximum umber of conditions for 'c_and' condition is 10"


def c_or(*conditions):
    """The intrinsic conditional function Fn::Or

    Returns true (for the pruposes of the cfn template) if any one of the specified conditions
    evaluate to true, or returns false if all of the conditions evaluates to false.

    Fn::Or acts as an OR operator.

    The minimum number of conditions that you can include is 2, and the maximum is 10.

    Args:
        *conditions: The conditions to evaluate

    """
    _validate_logical_condition_counts(c_or, conditions)
    return {'Fn::Or': list(conditions)}
c_or._errmsg_min = "Minimum umber of conditions for 'c_or' condition is 2"
c_or._errmsg_max = "Maximum umber of conditions for 'c_or' condition is 10"


def c_not(condition):
    """The intrinsic conditional function Fn::Not

    Returns true for a condition that evaluates to false or
    returns false for a condition that evaluates to true.

    Fn::Not acts as a NOT operator.

    """
    return {'Fn::Not': [condition]}


def c_equals(value_1, value_2):
    """The intrinsic conditional function Fn::Equals

    Compares if two values are equal.

    Returns true if the two values are equal or false if they aren't.

    """
    return {'Fn::Equals': [value_1, value_2]}


def c_if(condition_name, value_if_true, value_if_false):
    """The intrinsic conditional function Fn::If representsa a ternary conditional operator

    Returns one value if the specified condition evaluates to true and another value
    if the specified condition evaluates to false.

    Currently, AWS CloudFormation supports the Fn::If intrinsic function in the
    metadata attribute, update policy attribute, and property values in the Resources
    section and Outputs sections of a template.

    You can use the AWS::NoValue pseudo parameter as a return value
    to remove the corresponding property.

    """
    return {'Fn::If': [condition_name, value_if_true, value_if_false]}
