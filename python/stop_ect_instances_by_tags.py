import boto3
import sys
from utils import remove_hosts_from_ssh_config

def parse_tags(tag_str):
    tags = {}
    for tag_pair in tag_str.split():
        key, value = tag_pair.split('=')
        tags[key] = value
    return tags


def stop_ec2_instances_by_tags(tag_dict):
    ec2 = boto3.resource('ec2')

    filters = [{'Name': f'tag:{key}', 'Values': [value]} for key, value in tag_dict.items()]
    filters.append({'Name': 'instance-state-name', 'Values': ['running']})

    instances = ec2.instances.filter(Filters=filters)

    instance_names = []
    for instance in instances:
        print(f'Stopping instance {instance.id}')
        instance_name = get_instance_name(instance)
        instance.stop()
        instance_names.append(instance_name)

    return instance_names


def get_instance_name(instance):
    instance_name = "N/A"
    for tag in instance.tags:
        if tag["Key"] == "Name":
            instance_name = tag["Value"]
            break

    return instance_name


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python stop_ec2_instances_by_tags.py 'tag1=value1 tag2=value2 tag3=value3 ...'")
        sys.exit(1)

    tag_str = ' '.join(sys.argv[1:])
    tag_dict = parse_tags(tag_str)
    stopped_instance_names = stop_ec2_instances_by_tags(tag_dict)
    remove_hosts_from_ssh_config(stopped_instance_names)
