cft = CloudFormationTemplate(description='My project template.')

cft.parameters.add(
    Parameter('EC2InstanceType', 'String',
        {
            'Default': 'm1.small',
            'Description': 'Instance type to use for created Server EC2 instance',
            'AllowedPattern': 'm3.[a-z]+',
            'ConstraintDescription': 'Must use one of the m3 instance types.',
        }
    )
)

cft.resources.add(
    Resource('Server', 'AWS::EC2::Instance',
        {
            'ImageId': options['AmiId'],
            'InstanceType': ref('EC2InstanceType')
        }
    )
)

cft.resources.add(
    Resource('StaticFiles', 'AWS::S3::Bucket', {'AccessControl: PublicRead'}, Metadata(
        {'Object1': 'Location1', 'Object2': 'Location2'}
    ))
)
