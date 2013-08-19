cft = CloudFormationTemplate(description="A slightly more useful template.")

cft.resources.add(
    Resource('MyS3Bucket', 'AWS::S3::Bucket', None, Metadata(
        {"Object1": "Location1", "Object2": "Location2"}
    ))
)
