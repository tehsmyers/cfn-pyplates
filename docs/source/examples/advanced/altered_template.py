import sys

# If our base template isn't on the PYTHONPATH already, we need to do this:
sys.path.append('../path/to/base/templates')

import basetemplate

class AlteredTemplate(basetemplate.BaseTemplate):
    """This project only needs an S3 bucket, but no EC2 server."""

    def add_resources(self):
        self.add_bucket()

    def add_bucket(self):
        """This will add a bucket using the base template, and then add a custom CORS 
        configuration to it."""

        super(AlteredTemplate, self).add_bucket()
        self.resources['StaticFiles']['Properties']['CorsConfiguration'] = {
            'CorsRules': [
                {
                    'AllowedHeaders': ['*'],
                    'AllowedMethods': ['GET'],
                    'AllowedOrigins': ['*'],
                }
            ]
        }

cft = AlteredTemplate("S3 Bucket Project", options)
cft.add_resources()
