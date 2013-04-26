cft = CloudFormationTemplate(description="A self-referential template.")

cft.parameters.add(Parameter('ImageId', 'String',
    {
        'Default': 'ami-c30360aa',
        'Description': 'Amazon Machine Image ID to use for the created instance',
        'AllowedPattern': 'ami-[a-f0-9]+',
        'ConstraintDescription': 'must start with "ami-" followed by lowercase hexidecimal characters',
    })
)

cft.parameters.add(Parameter('InstanceName', 'String',
    {
        'Description': 'A name for the instance to be created',
    })
)

cft.parameters.add(Parameter('InstanceType', 'String',
    {
        'Default': 'm1.small',
    })
)

# Now the Resource definition is all refs, totally customizeable at
# stack creation
cft.resources.add(Resource('AnInstance', 'AWS::EC2::Instance',
    {
        'ImageId': ref('ImageId'),
        'InstanceType': ref('InstanceType'),
        'Tags': ec2_tags({
            'Name': ref('InstanceName'),
        })
    })
)

cft.outputs.add(Output('DnsName',
    get_att('AnInstance', 'PublicDnsName'),
    'The public DNS Name for AnInstance')
)
