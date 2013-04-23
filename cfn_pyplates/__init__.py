'''Pyplates: Python-generated cloudformation templates!

Class-based representations of cloudformation templates and resources, with
the goal of baking cloudformation templates based on input config files and
pythonic classes to represent the template resource hierarchy

'''

# Get all the useful bits in this namespace explicitly
from cfn_pyplates import exceptions
from cfn_pyplates.base import (
    BaseMapping,
    CloudFormationTemplate,
    Parameters,
    Mappings,
    Resources,
    Outputs,
)
from cfn_pyplates.functions import (
    base64,
    find_in_map,
    get_att,
    get_azs,
    join,
    select,
    ref,
)
