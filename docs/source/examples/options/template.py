description = 'My static webapp {0} stack'.format(options['StackRole'])
cft = CloudFormationTemplate(description)

# Make a load balancer
cft.resources.add(Resource('LoadBalancer',
    'AWS::ElasticLoadBalancing::LoadBalancer',
    {
        'AvailabilityZones': options['AppServerAvailabilityZones'],
        'HealthCheck': {
            'HealthyThreshold': '2',
            'Interval': '30',
            'Target': 'HTTP:80/',
            'Timeout': '5',
            'UnhealthyThreshold': '2'
        },
        'Listeners': [
            {
                'LoadBalancerPort': '80',
                'Protocol': 'HTTP',
                'InstanceProtocol': 'HTTP',
                'InstancePort': '80',
                'PolicyNames': []
            },
        ],
    })
)

# Make a security group for the load balancer
cft.resources.add(Resource('ELBSecurityGroup',
    'AWS::EC2::SecurityGroup',
    {
        'GroupDescription': 'allow traffic from our app servers to the load balancer'
    })
)

# Put an ingress policy on the load balancer security group
cft.resources.add(Resource('ELBSecurityGroupIngressHTTP',
    'AWS::EC2::SecurityGroupIngress',
    {
        'GroupName': ref('ELBSecurityGroup'),
        'IpProtocol': 'tcp',
        'FromPort': '80',
        'ToPort': '80',
        'SourceSecurityGroupName': get_att('LoadBalancer', 'SourceSecurityGroup.GroupName'),
        'SourceSecurityGroupOwnerId': get_att('LoadBalancer', 'SourceSecurityGroup.OwnerAlias')
    })
)

# Let folks SSH up to the instance
cft.resources.add(Resource('SSHSecurityGroup',
    'AWS::EC2::SecurityGroup',
    {
        'GroupDescription': 'allows inbound SSH from all',
        'SecurityGroupIngress': {
            'IpProtocol': 'tcp',
            'CidrIp': '0.0.0.0/0',
            'FromPort': '22',
            'ToPort': '22'
        }
    })
)

# Make our auto scaling group
cft.resources.add(Resource('AppServerAutoScalingGroup',
    'AWS::AutoScaling::AutoScalingGroup',
    {
        'AvailabilityZones': options['AppServerAvailabilityZones'],
        'HealthCheckGracePeriod': 300,
        'HealthCheckType': 'ELB',
        'LaunchConfigurationName': ref('AppServerAutoScalingLaunchConfig'),
        'LoadBalancerNames': [ref('LoadBalancer')],
        'MaxSize': options['AutoScalingGroupMaxSize'],
        'MinSize': options['AutoScalinggroupMinSize'],
        'Tags': [{
            'Key': 'Name',
            'Value': options['StackRole'] + '-static-app-server',
            'PropagateAtLaunch': True,
        }]
    })
)
# Create the auto scaling group configuration for managing the server instances
cft.resources.add(Resource('AppServerAutoScalingLaunchConfig',
    'AWS::AutoScaling::LaunchConfiguration',
    {
        'ImageId': options['ImageId'],
        'InstanceType': options['AppServerInstanceType'],
        'KeyName': options['KeyPair'],
        'SecurityGroups': [
            ref('ELBSecurityGroup'),
            ref('SSHSecurityGroup'),
        ],
        # Another way to pass a user-data script,
        # looks better than the first example, but it's more tedious
        'UserData': base64(join('\n',
            '#!/bin/bash -v',
            '# do stuff...',
            '# ',
            '# Like maybe kick off cfnbootstrap, using all of the',
            '# AWS:CloudFormation::Init Metadata That we could have',
            '# put on our AutoScalingGroup',
            'exit 0',
        ))
    })
)

# Scale up policy for when the scale up alarm trips
cft.resources.add(Resource('AppServerScaleUpPolicy',
    'AWS::AutoScaling::ScalingPolicy',
    {
        'AdjustmentType': 'ChangeInCapacity',
        'AutoScalingGroupName': ref('AppServerAutoScalingGroup'),
        'Cooldown': '600',
        'ScalingAdjustment': '1'
    })
)

# Scale down policy for when the scale down alarm trips
cft.resources.add(Resource('AppServerScaleDownPolicy',
    'AWS::AutoScaling::ScalingPolicy',
    {
        'AdjustmentType': 'ChangeInCapacity',
        'AutoScalingGroupName': ref('AppServerAutoScalingGroup'),
        'Cooldown': '600',
        'ScalingAdjustment': '-1'
    })
)

# CloudWatch scale up alarm for triggering scale events
cft.resources.add(Resource('AppServerCPUAlarmHigh',
    'AWS::CloudWatch::Alarm',
    {
        'AlarmDescription': 'Scale up if average CPU usage of the AppServers stays above 75% for at least 5 minutes',
        'Dimensions': [{'Name': 'AutoScalingGroupName', 'Value': ref('AppServerAutoScalingGroup')}],
        'Namespace': 'AWS/EC2',
        'MetricName': 'CPUUtilization',
        'Unit': 'Percent',
        'Period': '60',
        'EvaluationPeriods': '5',
        'Statistic': 'Average',
        'ComparisonOperator': 'GreaterThanThreshold',
        'Threshold': '75',
        'ActionsEnabled': options['CloudWatchAlarmActionsEnabled'],
        'AlarmActions': [ref('AppServerScaleUpPolicy')]
    })
)

# CloudWatch scale down alarm for triggering scale events
cft.resources.add(Resource('AppServerCPUAlarmLow',
    'AWS::CloudWatch::Alarm',
    {
        'AlarmDescription': 'Scale down if average CPU usage of the AppServers stays below 25% for at least 5 minutes',
        'Dimensions': [{'Name': 'AutoScalingGroupName', 'Value': ref('AppServerAutoScalingGroup')}],
        'Namespace': 'AWS/EC2',
        'MetricName': 'CPUUtilization',
        'Unit': 'Percent',
        'Period': '60',
        'EvaluationPeriods': '5',
        'Statistic': 'Average',
        'ComparisonOperator': 'LessThanThreshold',
        'Threshold': '25',
        'ActionsEnabled': options['CloudWatchAlarmActionsEnabled'],
        'AlarmActions': [ref('AppServerScaleUpPolicy')]
    })
)

# Add the load balancer endpoint to our outputs
cft.outputs.add(
    Output('LoadBalancerEndpoint',
        get_att('LoadBalancer', 'DNSName')
    )
)
