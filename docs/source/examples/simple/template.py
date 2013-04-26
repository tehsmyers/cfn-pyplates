# Start with a template...
cft = CloudFormationTemplate(description="A very small template.")

cft.resources.ec2_instance = Resource('AnInstance', 'AWS::EC2::Instance',
    Properties({
        # This is an ubuntu AMI, picked from http://cloud-images.ubuntu.com/
        # You may need to change this if you're not in the us-east-1 region
        # Or if Ubuntu deregisters the AMI
        'ImageID': 'ami-c30360aa',
        'InstanceType': 'm1.small',
    })
)
