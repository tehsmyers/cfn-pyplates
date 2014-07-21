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

from ordereddict import OrderedDict

from cfn_pyplates.exceptions import AddRemoveError

aws_template_format_version = '2010-09-09'

__all__ = [
    'JSONableDict',
    'CloudFormationTemplate',
    'Parameters',
    'Mappings',
    'Resources',
    'Outputs',
    'Properties',
    'Mapping',
    'Resource',
    'Parameter',
    'Output',
    'DependsOn',
    'DeletionPolicy',
    'UpdatePolicy',
    'Metadata',
    'ec2_tags',
    'Conditions',
    'Condition',
    'ConditionItem',
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
            try:
                self.remove(attr)
            except KeyError:
                # Key already deleted, somehow.
                # Everything's fine here now. How're you?
                pass
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
            raise AddRemoveError

        return child

    def remove(self, child):
        """Remove a child node

        Args:
            child: An instance of JSONableDict

        Raises:
            AddRemoveError: :exc:`cfn_pyplates.exceptions.AddRemoveError`

        """
        if isinstance(child, JSONableDict):
            del(self[child.name])
        else:
            raise AddRemoveError

    def to_json(self, *args, **kwargs):
        """Thin wrapper around the :func:`json.dumps` method.

        Allows for passing any arguments that json.dumps would accept to
        completely customize the JSON output if desired.

        """
        return json.dumps(self, *args, **kwargs)


class CloudFormationTemplate(JSONableDict):
    """The root element of a CloudFormation template [#cfn-template]_

    Takes an option description string in the constructor
    Comes pre-loaded with all the subelements CloudFormation can stand:

    - Parameters
    - Mappings
    - Resources
    - Outputs
    - Conditions

    """
    def __init__(self, description=None):
        super(CloudFormationTemplate, self).__init__({
            'AWSTemplateFormatVersion': aws_template_format_version,
        })
        if description:
            self.update({
                'Description': description,
            })
        # Tack on all the base template elements that a CF template can handle
        # at easy-to-reach parameters
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


class Metadatums(JSONableDict):
    """The base Container for metadatums used at stack creation [#cfn-metadata]_

    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`
    """
    pass


# CloudFormationTemplate base elements
class Parameters(JSONableDict):
    """The base Container for parameters used at stack creation [#cfn-parameters]_

    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`
    """
    pass


class Mappings(JSONableDict):
    """The base Container for stack option mappings [#cfn-mappings]_

    .. note::

        Since most lookups can be done inside a pyplate using python,
        this is normally unused.

    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`
    """
    pass


class Resources(JSONableDict):
    """The base Container for stack resources [#cfn-resources]_

    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`
    """
    pass


class Outputs(JSONableDict):
    """The base Container for stack outputs [#cfn-outputs]_

    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`
    """
    pass

class Conditions(JSONableDict):
    """The base Container for stack conditions used at stack creation [#cfn-conditions]_
        
    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`
    """
    pass


# Other 'named' JSONableDicts
class Properties(JSONableDict):
    """A properties mapping [#cfn-properties]_, used by various CFN declarations

    Can be found in:

    - :class:`cfn_pyplates.core.Parameters`
    - :class:`cfn_pyplates.core.Outputs`
    - :class:`cfn_pyplates.core.Resource`

    Properties will be most commonly found in Resources
    """
    pass


class Resource(JSONableDict):
    """A generic CFN Resource [#cfn-resource-types]_

    Used in the :class:`cfn_pyplates.core.Resources` container.

    All resources have a name, and most have a 'Type' and 'Properties' dict.
    Thus, this class takes those as arguments and makes a generic resource.

    The 'name' parameter must follow CFN's guidelines for naming [#cfn-resources]_
    The 'type' parameter must be one of these:

    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html

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

    """

    def __init__(self, name, type, properties=None, attributes=[]):
        update_dict = {'Type': type}
        super(Resource, self).__init__(update_dict, name)
        if properties:
            try:
                # Assume we've got a JSONableDict
                self.add(properties)
            except AddRemoveError:
                # If not, coerce it
                self.add(Properties(properties))
        if attributes:
            if self._is_attribute(attributes):
                self.add(attributes)
            elif isinstance(attributes, list):
                for i in attributes:
                    if isinstance(i, JSONableDict) and self._is_attribute(i):
                        self.add(i)

    def _is_attribute(self, attribute):
        """Is the Object a valid Resource Attribute?
        :param attribute: the object under test
        """
        if isinstance(attribute, list):
            for i in attribute:
                self._is_attribute(i)
        elif attribute.__class__.__name__ in ['Metadata', 'UpdatePolicy']:
            self.add(attribute)
        elif attribute.__class__.__name__ in ['DependsOn', 'DeletionPolicy', 'Condition']:
            self.update({attribute.__class__.__name__: attribute.value})


class Parameter(JSONableDict):
    """A CFN Parameter [#cfn-parameters]_

    Used in the :class:`cfn_pyplates.core.Parameters` container, a Parameter
    will be used when the template is processed by CloudFormation to prompt the
    user for any additional input.

    More information for Parameter options:

    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html

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
    """A CFN Mapping [#cfn-mappings]_

    Used in the :class:`cfn_pyplates.core.Mappings` container, a Mapping
    defines mappings used within the Cloudformation template and is not
    the same as a PyPlates options mapping.

    More information for mapping options:

    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/concept-mappings.html

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
    """A CFN Output [#cfn-outputs]_

    Used in the :class:`cfn_pyplates.core.Outputs`, an Output entry describes
    a value to be shown when describe this stack using CFN API tools.

    More information for Output options can be found here:

    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html

    Args:
        name: The unique name of the output
        value: The value the output should return
        description: An optional description of this output

    """

    def __init__(self, name, value, description=None):
        update_dict = {'Value': value}
        if description is not None:
            update_dict['Description'] = description
        super(Output, self).__init__(update_dict, name)


class Metadata(JSONableDict):
    """A CFN Output [#cfn-outputs]_

    Used in the :class:`cfn_pyplates.core.Resource`,The Metadata attribute enables you to associate
    structured data with a resource. By adding a Metadata attribute to a resource, you can add data
    in JSON format to the resource declaration. In addition, you can use intrinsic functions (such
    as GetAtt and Ref), parameters, and pseudo parameters within the Metadata attribute to add those
    interpreted values.

    More information for Metadata can be found here:

    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-metadata.html

    Args:
        properties: The unique name of the output

    """

    def __init__(self, properties=None):
        super(Metadata, self).__init__(properties, 'Metadata')


class DependsOn(object):
    """A CFN Output [#cfn-outputs]_

    Used in the :class:`cfn_pyplates.core.Resource`, The DependsOn attribute enables you to specify
    that the creation of a specific resource follows another

    More information for DependsOn Attribute can be found here:

    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html

    Args:
        properties: The unique name of the output

    """

    def __init__(self, policy=None):
        if policy:
            self.value = policy


class DeletionPolicy(object):
    """A CFN Output [#cfn-outputs]_

    Used in the :class:`cfn_pyplates.core.Resource`, The DeletionPolicy attribute enables you to
    specify how AWS CloudFormation handles the resource deletion.

    More information for DeletionPolicy Attribute can be found here:

    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html

    Args:
        properties: The unique name of the output

    """

    def __init__(self, policy=None):
        if policy:
            self.value = str(policy)


class UpdatePolicy(JSONableDict):
    """A CFN Output [#cfn-outputs]_

    Used in the :class:`cfn_pyplates.core.Resource`, The UpdatePolicy attribute enables you to
    specify how AWS CloudFormation handles rolling updates for a particular resource.

    More information for UpdatePolicy Attribute can be found here:

    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html

    Args:
        properties: The unique name of the output

    """

    def __init__(self, properties=None):
        super(UpdatePolicy, self).__init__(properties, 'UpdatePolicy')


class Condition(object):
    """A CFN Output [#cfn-outputs]_
    
    Used in the :class:`cfn_pyplates.core.Conditions`, The Condition attribute enables you to
    conditionally create resources based on the result of a ConditionItem.
    
    More information for Condition Attribute can be found here:
    
    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html
    
    Args:
    properties: The unique name of ConditionItem
    
    """
    
    def __init__(self, policy=None):
        if policy:
            self.value = policy


class ConditionItem(JSONableDict):
    """A CFN Parameter [#cfn-outputs]_
 
    Used in the :class:`cfn_pyplates.core.Condition` container, a ConditionItem
    will be used when the template is processed by CloudFormation so you can define which resources are
    created and how they're configured for each environment type.
    
    More information for ConditionItem options:
    
    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-conditions.html
    
    Args:
    name: The unique name of the ConditionItem to add
    type: The type of this parameter
    properties: The Intrinsic Conditional function
    
    """

    def __init__(self, name, type, conditions=None):
        # Just like a Resource, except the properties go in the
        # update_dict, not a named key.
        update_dict = {}
        if conditions is not None:
            update_dict.update(conditions)
        super(ConditionItem, self).__init__(update_dict, name)


def ec2_tags(tags):
    """A container for Tags on EC2 Instances

    Tags are declared really verbosely in CFN templates, but we have
    opportunites in the land of python to keep things a little more
    sane.

    So we can turn the
    `AWS EC2 Tags example <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/\
        aws-properties-ec2-tags.html>`_
    from this::

        "Tags": [
            { "Key" : "Role", "Value": "Test Instance" },
            { "Key" : "Application", "Value" : { "Ref" : "AWS::StackName"} }
        ]

    Into something more like this::

        EC2Tags({
            'Role': 'Test Instance',
            'Application': ref('StackName'),
        })

    Args:
        tags: A dictionary of tags to apply to an EC2 instance

    """
    tags_list = list()
    for key, value in tags.iteritems():
        tags_list.append({'Key': key, 'Value': value})

    return tags_list
