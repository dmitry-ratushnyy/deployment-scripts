import boto3
from utils import remove_hosts_from_ssh_config, get_instance_name


def terminate_all_ec2_instances():
    ec2 = boto3.resource('ec2')

    # Retrieve all instances
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['pending', 'running', 'stopping', 'stopped']}]
    )

    instance_names = []
    # Terminate all instances
    for instance in instances:
        print(f'Terminating instance {instance.id}')
        instance_name = get_instance_name(instance)
        instance.terminate()
        instance_names.append(instance_name)

    return instance_names


if __name__ == '__main__':
    terminated_instance_names = terminate_all_ec2_instances()
    remove_hosts_from_ssh_config(terminated_instance_names)
