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
]

class JSONableDict(OrderedDict):
    # Override these in instancees
    # Class Identifier MUST match the documented CloudFormation type name
    def __init__(self, update_dict=None):
        super(JSONableDict, self).__init__()
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
                pass
        super(JSONableDict, self).__delattr__(name)

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def json(self):
        return self.to_json(indent=2, separators=(',', ': '))

    def add(self, child):
        if isinstance(child, JSONableDict):
            self.update(
                {child.name: child}
            )
        else:
            raise AddRemoveError

    def remove(self, child):
        if isinstance(child, JSONableDict):
            del(self[child.name])
        else:
            raise AddRemoveError

    def to_json(self, *args, **kwargs):
        return json.dumps(self, *args, **kwargs)


class CloudFormationTemplate(JSONableDict):
    '''The root element of a CloudFormation template

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


# Stack'o'Mappings for CloudFormationTemplate
class Parameters(JSONableDict): pass
class Mappings(JSONableDict): pass
class Resources(JSONableDict): pass
class Outputs(JSONableDict): pass

