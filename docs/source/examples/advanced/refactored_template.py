class ProjectTemplate(CloudFormationTemplate):

    def add_resources(self):
        self.add_server()
        self.add_bucket()

    def add_server(self):
        self.parameters.add(
            Parameter('EC2InstanceType', 'String',
                {
                    'Default': 'm1.small',
                    'Description': 'Instance type to use for created Server EC2 instance',
                    'AllowedPattern': 'm3.[a-z]+',
                    'ConstraintDescription': 'Must use one of the m3 instance types.',
                }
            )
        )
        self.resources.add(
            Resource('Server', 'AWS::EC2::Instance',
                {
                    'ImageId': 'ami-c30360aa',
                    'InstanceType': ref('EC2InstanceType')
                }
            )
        )

    def add_bucket(self):
        self.resource.add(
            Resource('StaticFiles', 'AWS::S3::Bucket', {'AccessControl: PublicRead'}, Metadata(
                {'Object1': 'Location1', 'Object2': 'Location2'}
            ))
        )

cft = ProjectTemplate(description='My project template.')
cft.add_resources()
