import boto3
import sys
from utils import update_ssh_config

def start_ec2_instances_by_tags(tag_dict):
    ec2 = boto3.resource('ec2')

    filters = [{'Name': f'tag:{key}', 'Values': [value]} for key, value in tag_dict.items()]
    filters.append({'Name': 'instance-state-name', 'Values': ['stopped']})

    instances = ec2.instances.filter(Filters=filters)

    filtered_data = {
        "all": {
            "hosts": []
        }
    }

    for instance in instances:
        print(f'Starting instance {instance.id}')
        instance_name = get_instance_name(instance)
        instance.start()

        filtered_host = {
            "instance_name": instance_name,
            "public_ip": instance.public_ip_address,
            "public_dns": instance.public_dns_name
        }
        filtered_data["all"]["hosts"].append(filtered_host)

    return filtered_data

def get_instance_name(instance):
    instance_name = "N/A"
    for tag in instance.tags:
        if tag["Key"] == "Name":
            instance_name = tag["Value"]
            break

    return instance_name


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python start_ec2_instances_by_tags.py tag_key1=tag_value1 [tag_key2=tag_value2 ...]")
        sys.exit(1)

    tag_dict = {}
    for tag_pair in sys.argv[1:]:
        key, value = tag_pair.split('=')
        tag_dict[key] = value

    started_instances_data = start_ec2_instances_by_tags(tag_dict)
    update_ssh_config(started_instances_data)
