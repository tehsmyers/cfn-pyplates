cft = CloudFormationTemplate(description="A slightly more useful template.")

user_data_script = '''#!/bin/bash

echo "You can put your userdata script right here!"
'''

cft.resources.add(Resource('AnInstance', 'AWS::EC2::Instance',
    {
        'ImageId': 'ami-c30360aa',
        'InstanceType': 'm1.small',
        'UserData': base64(user_data_script),
    })
)
