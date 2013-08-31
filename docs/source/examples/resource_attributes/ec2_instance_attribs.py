user_data_script = '''#!/bin/bash

echo "You can put your userdata script right here!"
'''

cft = CloudFormationTemplate(description="A slightly more useful template.")
properties = {
    'ImageId': 'ami-c30360aa',
    'InstanceType': 'm1.small',
    'UserData': base64(user_data_script),
}
attributes = [
    Metadata({"packages": {}, "sources": {}, "commands": {}, "files": {}, "services": {}, "users": {}, "groups": {}}),
    UpdatePolicy({"MaxBatchSize": "", "MinInstancesInService": "", "PauseTime": ""}),
    DeletionPolicy("Retain"),
    DependsOn("myDB")
]
cft.resources.add(
    Resource('MyInstance', 'AWS::EC2::Instance', properties, attributes)
)
