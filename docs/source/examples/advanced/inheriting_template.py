import sys

# If our base template isn't on the PYTHONPATH already, we need to do this:
sys.path.append('../path/to/base/templates')

import basetemplate

class InheritingTemplate(basetemplate.BaseTemplate):
    def add_resources(self):
        self.add_server()
        self.add_bucket()

cft = InheritingTemplate("Our usual project", options)
cft.add_resources()

