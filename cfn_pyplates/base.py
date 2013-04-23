import inspect
import json

from ordereddict import OrderedDict

from cfn_pyplates.exceptions import AddRemoveError

aws_template_format_version = '2010-09-09'

__all__ = [
    'BaseMapping',
    'CloudFormationTemplate',
    'Parameters',
    'Mappings',
    'Resources',
    'Outputs',
]

class BaseMapping(OrderedDict):
    # Override these in instancees
    # Class Identifier MUST match the documented CloudFormation type name
    def __init__(self, update_dict=None):
        super(BaseMapping, self).__init__()
        if update_dict:
            self.update(update_dict)

    def __unicode__(self):
        # Indenting to keep things readable
        # Annoying trailing whitespace after commas removed
        # (The space after colons is cool, though. He can stay.)
        return unicode(json.dumps(self, indent=2, separators=(',', ': ')))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __setattr__(self, name, value):
        # This makes it simple to bind child dictionaries to an
        # attribute while still making sure they wind up in the output
        # dictionary, see usage example in CloudFormationTemplate init
        if isinstance(value, BaseMapping):
            self.add(value)
        super(BaseMapping, self).__setattr__(name, value)

    def __delattr__(self, name):
        attr = getattr(self, name)
        if isinstance(attr, BaseMapping):
            try:
                self.remove(attr)
            except KeyError:
                pass
        super(BaseMapping, self).__delattr__(name)

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def json(self):
        return json.dumps(self)

    def add(self, child):
        if isinstance(child, BaseMapping):
            self.update(
                {child.name: child}
            )
        else:
            raise AddRemoveError

    def remove(self, child):
        if isinstance(child, BaseMapping):
            del(self[child.name])
        else:
            raise AddRemoveError


class CloudFormationTemplate(BaseMapping):
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
            '''getmembers predicate to find empty BaseMapping attributes attached to self

            CloudFormation doesn't like empty mappings for these top-level
            attributes, so any falsey BaseMapping that's at attribute on
            the CloudFormationTemplate instance needs to get removed

            '''
            if isinstance(obj, BaseMapping) and not obj:
                return True
        for attr, mapping in inspect.getmembers(self, predicate):
            delattr(self, attr)

        return super(CloudFormationTemplate, self).__unicode__()


# Stack'o'Mappings for CloudFormationTemplate
class Parameters(BaseMapping): pass
class Mappings(BaseMapping): pass
class Resources(BaseMapping): pass
class Outputs(BaseMapping): pass


