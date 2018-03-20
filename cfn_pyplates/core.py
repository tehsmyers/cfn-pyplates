# Copyright (c) 2013 MetaMetrics, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

"""Core functionality and all required components of a working CFN template.

These are all available without preamble in a pyplate's global namespace.
"""
import inspect
import json
import traceback
import warnings
from collections import OrderedDict

from cfn_pyplates import exceptions
import functions

aws_template_format_version = '2010-09-09'

__all__ = [
    'JSONableDict',
    'CloudFormationTemplate',
    'Parameters',
    'Mappings',
    'Resources',
    'Outputs',
    'Conditions',
    'Properties',
    'Mapping',
    'Resource',
    'Parameter',
    'Output',
    'DependsOn',
    'CreationPolicy',
    'DeletionPolicy',
    'UpdatePolicy',
    'Metadata',
    'Condition',
    'ec2_tags',
]


class JSONableDict(OrderedDict):
    """A dictionary that knows how to turn itself into JSON

    Args:
        update_dict: A dictionary of values for prepopulating the JSONableDict
            at instantiation
        name: An optional name. If left out, the class's (or subclass's) name
            will be used.

    The most common use-case of any JSON entry in a CFN Template is the
    ``{"Name": {"Key1": "Value1", "Key2": Value2"} }`` pattern. The
    significance of a JSONableDict's subclass name, or explicitly passing
    a 'name' argument is accomodating this pattern. All JSONableDicts have
    names.

    To create the pyplate equivalent of the above JSON, contruct a
    JSONableDict accordingly::

        JSONableDict({'Key1': 'Value1', 'Key2', 'Value2'}, 'Name'})

    Based on :class:`ordereddict.OrderedDict`, the order of keys is significant.

    """
    def __init__(self, update_dict=None, name=None):
        super(JSONableDict, self).__init__()
        self._name = name

        if update_dict:
            self.update(update_dict)

    def __unicode__(self):
        # Indenting to keep things readable
        # Trailing whitespace after commas removed
        # (The space after colons is cool, though. He can stay.)
        return unicode(self.json)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __setattr__(self, name, value):
        # This makes it simple to bind child dictionaries to an
        # attribute while still making sure they wind up in the output
        # dictionary, see usage example in CloudFormationTemplate init
        if isinstance(value, JSONableDict):
            self.add(value)
        super(JSONableDict, self).__setattr__(name, value)

    def __delattr__(self, name):
        attr = getattr(self, name)
        if isinstance(attr, JSONableDict):
            self.remove(attr)
        super(JSONableDict, self).__delattr__(name)

    def _get_name(self):
        if self._name is not None:
            return self._name
        else:
            # Default to the class name if _name is None
            return self.__class__.__name__

    def _set_name(self, name):
        self._name = name

    def _del_name(self):
        self._name = None

    name = property(_get_name, _set_name, _del_name)
    """Accessor to the ``name`` internals;

    Allows getting, settings, and deleting the name
    """

    @property
    def json(self):
        'Accessor to the canonical JSON representation of a JSONableDict'
        return self.to_json(indent=2, separators=(',', ': '))

    def add(self, child):
        """Add a child node

        Args:
            child: An instance of JSONableDict

        Raises:
            AddRemoveError: :exc:`cfn_pyplates.exceptions.AddRemoveError`

        """
        if isinstance(child, JSONableDict):
            self.update(
                {child.name: child}
            )
        else:
            raise exceptions.AddRemoveError

        return child

    def remove(self, child):
        """Remove a child node

        Args:
            child: An instance of JSONableDict

        Raises:
            AddRemoveError: :exc:`cfn_pyplates.exceptions.AddRemoveError`

        """
        if isinstance(child, JSONableDict):
            try:
                del(self[child.name])
            except KeyError:
                # This will KeyError if the name of a child is changed but its
                # corresponding key in this dict is not updated. In normal usage,
                # this should never happen. If it does happen, you're doing
                # weird stuff, and have been warned.
                warnings.warn('{0} not found in dict when attempting removal'.format(child.name))
        else:
            raise exceptions.AddRemoveError

    def to_json(self, *args, **kwargs):
        """Thin wrapper around the :func:`json.dumps` method.

        Allows for passing any arguments that json.dumps would accept to
        completely customize the JSON output if desired.

        """
        return json.dumps(self, *args, **kwargs)


class CloudFormationTemplate(JSONableDict):
    """The root element of a CloudFormation template

    Takes an option description string in the constructor
    Comes pre-loaded with all the subelements CloudFormation can stand:

    - Metadata
    - Parameters
    - Mappings
    - Resources
    - Outputs
    - Conditions

    For more information, see `the AWS docs <cfn-template_>`_


    """
    def __init__(self, description=None, options=None):
        super(CloudFormationTemplate, self).__init__({
            'AWSTemplateFormatVersion': aws_template_format_version,
        })
        if description:
            self.update({
                'Description': description,
            })
        # Tack on all the base template elements that a CF template can handle
        # at easy-to-reach parameters
        self.options = options
        self.metadata = Metadata()
        self.parameters = Parameters()
        self.mappings = Mappings()
        self.resources = Resources()
        self.outputs = Outputs()
        self.conditions = Conditions()

    def __unicode__(self):
        # Before outputting to json, remove empty elements
        def predicate(obj):
            """getmembers predicate to find empty JSONableDict attributes attached to self

            CloudFormation doesn't like empty mappings for these top-level
            attributes, so any falsey JSONableDict that's at attribute on
            the CloudFormationTemplate instance needs to get removed

            """
            if isinstance(obj, JSONableDict) and not obj:
                return True
        for attr, mapping in inspect.getmembers(self, predicate):
            delattr(self, attr)

        return super(CloudFormationTemplate, self).__unicode__()


# CloudFormationTemplate base elements
class Parameters(JSONableDict):
    """The base Container for parameters used at stack creation

    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`

    For more information, see `the AWS docs <cfn-parameters_>`_

    """
    pass


class Mappings(JSONableDict):
    """The base Container for stack option mappings

    .. note::

        Since most lookups can be done inside a pyplate using python,
        this is normally unused.

    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`

    For more information, see `the AWS docs <cfn-mappings_>`_

    """
    pass


class Resources(JSONableDict):
    """The base Container for stack resources

    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`

    For more information, see `the AWS docs <cfn-resources_>`_

    """
    pass


class Outputs(JSONableDict):
    """The base Container for stack outputs

    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`

    For more information, see `the AWS docs <cfn-outputs_>`_

    """
    pass


class Conditions(JSONableDict):
    """The base Container for stack conditions used at stack creation

    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`

    For more information, see `the AWS docs <cfn-conditions_>`_

    """
    pass


# Other 'named' JSONableDicts
class Properties(JSONableDict):
    """A properties mapping, used by various CFN declarations

    Can be found in:

    - :class:`cfn_pyplates.core.Parameters`
    - :class:`cfn_pyplates.core.Outputs`
    - :class:`cfn_pyplates.core.Resource`

    Properties will be most commonly found in Resources

    For more information, see `the AWS docs <cfn-properties_>`_

    """
    pass


class Resource(JSONableDict):
    """A generic CFN Resource

    Used in the :class:`cfn_pyplates.core.Resources` container.

    All resources have a name, and most have a 'Type' and 'Properties' dict.
    Thus, this class takes those as arguments and makes a generic resource.

    The 'name' parameter must follow CFN's guidelines for naming
    The 'type' parameter must be `one of these <cfn-resource-types_>`_

    The optional 'properties' parameter is a dictionary of properties as
    defined by the resource type, see documentation related to each resource
    type

    Args:
        name: The unique name of the resource to add
        type: The type of this resource
        properties: Optional properties mapping to apply to this resource,
            can be an instance of ``JSONableDict`` or just plain old ``dict``
        attributes: Optional (one of 'Condition', 'DependsOn', 'DeletionPolicy',
            'Metadata', 'UpdatePolicy' or a list of 2 or more)

    For more information, see `the AWS docs <cfn-resources_>`_

    """

    def __init__(self, name, type, properties=None, attributes=[]):
        update_dict = {'Type': type}
        super(Resource, self).__init__(update_dict, name)
        if properties:
            try:
                # Assume we've got a JSONableDict
                self.add(properties)
            except exceptions.AddRemoveError:
                # If not, coerce it
                self.add(Properties(properties))
        if attributes:
            self._add_attributes(attributes)

    def _add_attributes(self, attribute):
        """Is the Object a valid Resource Attribute?
        :param attribute: the object under test
        """
        if isinstance(attribute, list):
            for attr in attribute:
                self._add_attributes(attr)
        elif attribute.__class__.__name__ in ['Metadata', 'UpdatePolicy', 'CreationPolicy']:
            self.add(attribute)
        elif attribute.__class__.__name__ in ['DependsOn', 'DeletionPolicy', 'Condition']:
            self.update({attribute.__class__.__name__: attribute.value})


class Parameter(JSONableDict):
    """A CFN Parameter

    Used in the :class:`cfn_pyplates.core.Parameters` container, a Parameter
    will be used when the template is processed by CloudFormation to prompt the
    user for any additional input.

    For more information, see `the AWS docs <cfn-parameters_>`_

    Args:
        name: The unique name of the parameter to add
        type: The type of this parameter
        properties: Optional properties mapping to apply to this parameter

    """

    def __init__(self, name, type, properties=None):
        # Just like a Resource, except the properties go in the
        # update_dict, not a named key.
        update_dict = {'Type': type}
        if properties is not None:
            update_dict.update(properties)
        super(Parameter, self).__init__(update_dict, name)


class Mapping(JSONableDict):
    """A CFN Mapping

    Used in the :class:`cfn_pyplates.core.Mappings` container, a Mapping
    defines mappings used within the Cloudformation template and is not
    the same as a PyPlates options mapping.

    For more information, see `the AWS docs <cfn-mappings_>`_

    Args:
        name: The unique name of the mapping to add
        mappings: The dictionary of mappings

    """

    def __init__(self, name, mappings=None):
        update_dict = {}
        if mappings is not None:
            update_dict.update(mappings)
        super(Mapping, self).__init__(update_dict, name)


class Output(JSONableDict):
    """A CFN Output

    Used in the :class:`cfn_pyplates.core.Outputs`, an Output entry describes
    a value to be shown when describe this stack using CFN API tools.

    For more information, see `the AWS docs <cfn-outputs_>`_

    Args:
        name: The unique name of the output
        value: The value the output should return
        description: An optional description of this output

    """

    def __init__(self, name, value, description=None, export_name=None):
        update_dict = {'Value': value}
        if description is not None:
            update_dict['Description'] = description
        if export_name is not None:
            update_dict['Export'] = {'Name': export_name}
        super(Output, self).__init__(update_dict, name)


class Metadata(JSONableDict):
    """CFN Metadata

    The Metadata attribute enables you to associate arbtrary data data with a template element (for
    example, a :class:`cfn_pyplates.core.Resource`. In addition, you can use intrinsic functions
    (such as GetAtt and Ref), parameters, and pseudo parameters within the Metadata attribute to
    add those interpreted values.

    For more information, see `the AWS docs <cfn-metadata_>`_

    """
    pass


class DependsOn(object):
    """A CFN Resource Dependency

    Used in the :class:`cfn_pyplates.core.Resource`, The DependsOn attribute enables you to specify
    that the creation of a specific resource follows another

    For more information, see `the AWS docs <cfn-dependson_>`_

    Args:
        properties: The unique name of the output

    """

    def __init__(self, policy=None):
        if policy:
            self.value = policy


class CreationPolicy(JSONableDict):
    """A CFN Resource Creation Policy

    Used in the :class:`cfn_pyplates.core.Resource`, The CreationPolicy attribute enables you to
    prevent a Resource's status reaching create complete until AWS CloudFormation receives a
    specified number of success signals or the timeout period is exceeded

    For more information, see `the AWS docs <cfn-creationpolicy_>`_

    Args:
        count: number of success signals AWS CloudFormation must receive before
            it sets the resource status as CREATE_COMPLETE
        timeout: The length of time that AWS CloudFormation waits for the number of signals that
            was specified in the count kwarg (see AWS docs for syntax)

    """
    def __init__(self, count=None, timeout=None):
        super(CreationPolicy, self).__init__(name='CreationPolicy')
        resource_signal = {}
        if count is not None:
            resource_signal['Count'] = int(count)
        if timeout is not None:
            resource_signal['Timeout'] = str(timeout)
        resource_signal = JSONableDict(resource_signal, 'ResourceSignal')
        self.add(resource_signal)


class DeletionPolicy(object):
    """A CFN Resource Deletion Policy

    Used in the :class:`cfn_pyplates.core.Resource`, The DeletionPolicy attribute enables you to
    specify how AWS CloudFormation handles the resource deletion.

    For more information, see `the AWS docs <cfn-deletionpolicy_>`_

    Args:
        properties: The unique name of the output

    """

    def __init__(self, policy=None):
        if policy:
            self.value = str(policy)


class UpdatePolicy(JSONableDict):
    """A CFN Resource Update Policy

    Used in the :class:`cfn_pyplates.core.Resource`, The UpdatePolicy attribute enables you to
    specify how AWS CloudFormation handles rolling updates for a particular resource.

    For more information, see `the AWS docs <cfn-updatepolicy_>`_

    Args:
        properties: The unique name of the output

    """

    def __init__(self, properties=None):
        super(UpdatePolicy, self).__init__(properties, 'UpdatePolicy')


class Condition(JSONableDict):
    """A CFN Condition Item

    Used in the :class:`cfn_pyplates.core.Condition` container, a ConditionItem
    will be used when the template is processed by CloudFormation so you can define
    which resources are created and how they're configured for each environment type.

    Conditions are made up of instrinsic functions for conditions found in
    :mod:`cfn_pyplates.functions`, or a :func:`ref <cfn_pyplates.functions.ref>`
    to a :class:`Parameter` or :class:`Mapping`.

    For more information, see `the AWS docs <cfn-conditions_>`_

    Args:
        name: The unique name of the ConditionItem to add
        type: The type of this parameter
        properties: The Intrinsic Conditional function

    """

    def __init__(self, name, condition):
        super(Condition, self).__init__(condition, name)
        self.value = name


def ec2_tags(tags):
    """A container for Tags on EC2 Instances

    Tags are declared really verbosely in CFN templates, but we have
    opportunites in the land of python to keep things a little more
    sane.

    So we can turn the AWS EC2 Tags example from this::

        "Tags": [
            { "Key" : "Role", "Value": "Test Instance" },
            { "Key" : "Application", "Value" : { "Ref" : "AWS::StackName"} }
        ]

    Into this::

        ec2_tags({
            'Role': 'Test Instance',
            'Application': ref('StackName'),
        })

    For more information, see `the AWS docs <cfn-ec2tags_>`_


    Args:
        tags: A dictionary of tags to apply to an EC2 instance

    """
    tags_list = list()
    for key, value in tags.iteritems():
        tags_list.append({'Key': key, 'Value': value})

    return tags_list


def generate_pyplate(pyplate, options=None):
    """Generate CloudFormation JSON Template based on a Pyplate

    Arguments:
      pyplate
        input pyplate file, can be a path or a file object

      options
        a mapping of some kind (probably a dict),
        to be used at this pyplate's options mapping

    Returns the output string of the compiled pyplate

    """
    try:
        if not isinstance(pyplate, file):
            pyplate = open(pyplate)
        pyplate = _load_pyplate(pyplate, options)
        cft = _find_cloudformationtemplate(pyplate)
        output = unicode(cft)
    except Exception:
        print 'Error processing the pyplate:'
        print traceback.format_exc()
        return None

    return output


def _load_pyplate(pyplate, options_mapping=None):
    'Load a pyplate file object, and return a dict of its globals'
    # Inject all the useful stuff into the template namespace
    exec_namespace = {
        'options': options_mapping,
    }
    for entry in __all__:
        exec_namespace[entry] = globals().get(entry)
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
        if isinstance(value, CloudFormationTemplate):
            return value

    # If we haven't returned something, it's an Error
    raise exceptions.Error('No CloudFormationTemplate found in pyplate')
