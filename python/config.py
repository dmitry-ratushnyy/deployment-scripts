import os

class Config:
    SSH_CONFIG_PATH = os.path.expanduser('~/.ssh/config')
    IDENTITY_FILE_PATH = os.path.abspath('../../keys/canonical/dmitry.ratushnyy@canonical__aws.pem')
    SSH_USER = "ubuntu"
    INVENTORY_PATH = './ansible/inventory_aws_ec2.yml'
