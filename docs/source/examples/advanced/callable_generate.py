# This isn't included in cfn_pyplates like most pyplate components;
# It must be imported explicitly
from cfn_pyplates.core import generate_pyplate

# Given the "project.py" example above, generate the pyplate
# directly in python
generate_pyplate('/path/to/project.py')

# In addition, if you already have a reference to a
# CloudFormationTemplate, generating its JSON template is as easy as
# casting it as a string (or unicode) object:
print str(my_cloud_formation_template_instance)
