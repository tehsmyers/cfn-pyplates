'''Core functionality and all required components of a working CFN template.

These are all available without preamble in a pyplate's global namespace.
'''
import inspect
import json

from ordereddict import OrderedDict

from cfn_pyplates.exceptions import AddRemoveError, Error

aws_template_format_version = '2010-09-09'

__all__ = [
    'JSONableDict',
    'CloudFormationTemplate',
    'Parameters',
    'Mappings',
    'Resources',
    'Outputs',
    'Properties',
    'Resource',
]

class JSONableDict(OrderedDict):
    '''A dictionary that knows how to turn itself into JSON

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

    '''
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
    '''Accessor to the ``name`` internals;

    Allows getting, settings, and deleting the name
    '''

    @property
    def json(self):
        'Accessor to the canonical JSON representation of a JSONableDict'
        return self.to_json(indent=2, separators=(',', ': '))

    def add(self, child):
        '''Add a child node

        Args:
            child: An instance of JSONableDict

        Raises:
            AddRemoveError: :exc:`cfn_pyplates.exceptions.AddRemoveError`

        '''
        if isinstance(child, JSONableDict):
            self.update(
                {child.name: child}
            )
        else:
            raise AddRemoveError

    def remove(self, child):
        '''Remove a child node

        Args:
            child: An instance of JSONableDict

        Raises:
            AddRemoveError: :exc:`cfn_pyplates.exceptions.AddRemoveError`

        '''
        if isinstance(child, JSONableDict):
            del(self[child.name])
        else:
            raise AddRemoveError

    def to_json(self, *args, **kwargs):
        '''Thin wrapper around the :func:`json.dumps` method.

        Allows for passing any arguments that json.dumps would accept to
        completely customize the JSON output if desired.

        '''
        return json.dumps(self, *args, **kwargs)


class CloudFormationTemplate(JSONableDict):
    '''The root element of a CloudFormation template [#cfn-template]_

    Takes an option description string in the constructor
    Comes pre-loaded with all the subelements CloudFormation can stand:

    - Parameters
    - Mappings
    - Resources
    - Outputs

    '''
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

    def __unicode__(self):
        # Before outputting to json, remove empty elements
        def predicate(obj):
            '''getmembers predicate to find empty JSONableDict attributes attached to self

            CloudFormation doesn't like empty mappings for these top-level
            attributes, so any falsey JSONableDict that's at attribute on
            the CloudFormationTemplate instance needs to get removed

            '''
            if isinstance(obj, JSONableDict) and not obj:
                return True
        for attr, mapping in inspect.getmembers(self, predicate):
            delattr(self, attr)

        return super(CloudFormationTemplate, self).__unicode__()


# CloudFormationTemplate base elements
class Parameters(JSONableDict):
    '''The base Container for parameters used at stack creation [#cfn-parameters]_

    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`
    '''
    pass

class Mappings(JSONableDict):
    '''The base Container for stack option mappings [#cfn-mappings]_

    .. note::

        Since most lookups can be done inside a pyplate using python,
        this is normally unused.

    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`
    '''
    pass



class Resources(JSONableDict):
    '''The base Container for stack resources [#cfn-resources]_

    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`
    '''
    pass



class Outputs(JSONableDict):
    '''The base Container for stack outputs [#cfn-outputs]_

    Attached to a :class:`cfn_pyplates.core.CloudFormationTemplate`
    '''
    pass



# Other 'named' JSONableDicts
class Properties(JSONableDict):
    '''A properties mapping [#cfn-properties]_, used by various CFN declarations

    Can be found in:

    - :class:`cfn_pyplates.core.Parameters`
    - :class:`cfn_pyplates.core.Outputs`
    - :class:`cfn_pyplates.core.Resource`

    Properties will be most commonly found in Resources
    '''
    pass

class Resource(JSONableDict):
    '''A generic CFN Resource [#cfn-resources]_

    Most resources have a name, and consist of a 'Type' and 'Properties' dict.
    Thus, this class takes those as arguments and makes a generic resource.

    The 'name' parameter must follow CFN's guidelines for naming, found `here <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resources-section-structure.html>`_
    The 'type' parameter must be one of the `CFN Resource Types <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html>`_.
    The optional 'properties' parameter is a dictionary of properties as defined by the resource type, see documentation references in the 'type' parameter.

    Args:
        name: The name of the resource to add
        type: The type of this resource
        properties: An optional properties mapping to apply to this resource,
            can be an instance of ``JSONableDict`` or just plain old ``dict``

    '''

    def __init__(self, name, type, properties=None):
        update_dict = {'Type': type}
        super(Resource, self).__init__(update_dict, name)
        if properties:
            try:
                # Assume we've got a JSONableDict
                self.add(properties)
            except AddRemoveError:
                # If not, coerce it
                self.add(Properties(properties))

