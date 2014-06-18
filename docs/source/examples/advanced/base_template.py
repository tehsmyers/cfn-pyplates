from pyplates import core, functions

class BaseTemplate(core.CloudFormationTemplate):

    def add_server(self):
        self.parameters.add(
            core.Parameter('EC2InstanceType', 'String',
                {
                    'Default': 'm1.small',
                    'Description': 'Instance type to use for created Server EC2 instance',
                    'AllowedPattern': 'm3.[a-z]+',
                    'ConstraintDescription': 'Must use one of the m3 instance types.',
                }
            )
        )
        self.resources.add(
            core.Resource('Server', 'AWS::EC2::Instance',
                {
                    'ImageId': self.options['AmiId'],
                    'InstanceType': functions.ref('EC2InstanceType')
                }
            )
        )

    def add_bucket(self):
        self.resource.add(
            core.Resource(
                'StaticFiles',
                'AWS::S3::Bucket',
                {'AccessControl: PublicRead'},
                Metadata({'Object1': 'Location1', 'Object2': 'Location2'})
            )
        )
