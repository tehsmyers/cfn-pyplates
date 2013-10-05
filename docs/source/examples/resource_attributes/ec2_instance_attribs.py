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
    Metadata(
        {
            "AWS::CloudFormation::Init": {
                "config": {
                    "packages": {
                        "rpm": {
                            "epel": "http://download.fedoraproject.org/pub/epel/5/i386/epel-release-5-4.noarch.rpm"
                        },
                        "yum": {
                            "httpd": [],
                            "php": [],
                            "wordpress": []
                        },
                        "rubygems": {
                            "chef": ["0.10.2"]
                        }
                    },
                    "sources": {
                        "/etc/puppet": "https://github.com/user1/cfn-demo/tarball/master"
                    },
                    "commands": {
                        "test": {
                            "command": "echo \"$CFNTEST\" > test.txt",
                            "env": {"CFNTEST": "I come from config1."},
                            "cwd": "~",
                            "test": "test ! -e ~/test.txt",
                            "ignoreErrors": "false"
                        }
                    },
                    "files": {
                        "/tmp/setup.mysql": {
                            "content":
                                join('',
                                     "CREATE DATABASE ", ref("DBName"), ";\n",
                                     "CREATE USER '", ref("DBUsername"), "'@'localhost' IDENTIFIED BY '",
                                     ref("DBPassword"),
                                     "';\n",
                                     "GRANT ALL ON ", ref("DBName"), ".* TO '", ref("DBUsername"), "'@'localhost';\n",
                                     "FLUSH PRIVILEGES;\n"
                                ),
                            "mode": "000644",
                            "owner": "root",
                            "group": "root"
                        }
                    },
                    "services": {
                        "sysvinit": {
                            "nginx": {
                                "enabled": "true",
                                "ensureRunning": "true",
                                "files": ["/etc/nginx/nginx.conf"],
                                "sources": ["/var/www/html"]
                            },
                            "php-fastcgi": {
                                "enabled": "true",
                                "ensureRunning": "true",
                                "packages": {
                                    "yum": ["php", "spawn-fcgi"]
                                }
                            },
                            "sendmail": {
                                "enabled": "false",
                                "ensureRunning": "false"
                            }
                        }
                    },
                    "users": {
                        "myUser": {
                            "groups": ["groupOne", "groupTwo"],
                            "uid": "50",
                            "homeDir": "/tmp"
                        }
                    },
                    "groups": {
                        "groupOne": {
                        },
                        "groupTwo": {
                            "gid": "45"
                        }
                    }
                }
            }
        }
    ),
    UpdatePolicy(
        {
            "AutoScalingRollingUpdate": {
                "MinInstancesInService": "1",
                "MaxBatchSize": "1",
                "PauseTime": "PT12M5S"
            }
        }
    ),
    DeletionPolicy("Retain"),
    DependsOn(ref("myDB"))
]
cft.resources.add(
    Resource('MyInstance', 'AWS::EC2::Instance', properties, attributes)
)
