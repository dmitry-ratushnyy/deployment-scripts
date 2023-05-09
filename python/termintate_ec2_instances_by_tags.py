import boto3
import sys
from utils import remove_hosts_from_ssh_config, get_instance_name


def terminate_ec2_instances_by_tags(tag_dict):
    ec2 = boto3.resource('ec2')

    filters = [{'Name': f'tag:{key}', 'Values': [value]} for key, value in tag_dict.items()]
    filters.append({'Name': 'instance-state-name', 'Values': ['running', 'stopped', 'stopping']})

    instances = ec2.instances.filter(Filters=filters)

    instance_names = []
    for instance in instances:
        print(f'Terminating instance {instance.id}')
        instance_name = get_instance_name(instance)
        instance.terminate()
        instance_names.append(instance_name)

    return instance_names


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python terminate_ec2_instances_by_tags.py tag_key1=tag_value1 [tag_key2=tag_value2 ...]")
        sys.exit(1)

    tag_dict = {}
    for tag_pair in sys.argv[1:]:
        key, value = tag_pair.split('=')
        tag_dict[key] = value

    terminated_instance_names = terminate_ec2_instances_by_tags(tag_dict)
    remove_hosts_from_ssh_config(terminated_instance_names)
