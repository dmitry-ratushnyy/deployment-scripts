import re
from config import Config

def update_ssh_config(filtered_data):
    ssh_config_lines = []
    for host in filtered_data["all"]["hosts"]:
        ssh_config_lines.append(f"Host {host['instance_name']}")
        ssh_config_lines.append(f"  HostName {host['public_dns']}")
        ssh_config_lines.append(f"  User {Config.SSH_USER}")
        ssh_config_lines.append(f"  IdentityFile {Config.IDENTITY_FILE_PATH}")
        ssh_config_lines.append("")

    with open(Config.SSH_CONFIG_PATH, 'a') as ssh_config_file:
        ssh_config_file.write("\n".join(ssh_config_lines))


def remove_hosts_from_ssh_config(instance_names):
    with open(Config.SSH_CONFIG_PATH, 'r') as ssh_config_file:
        ssh_config_lines = ssh_config_file.readlines()

    new_ssh_config_lines = []
    skip_next_lines = 0
    for line in ssh_config_lines:
        if skip_next_lines > 0:
            skip_next_lines -= 1
            continue

        matched_instance_name = None
        for instance_name in instance_names:
            if re.search(f"Host {instance_name}", line):
                matched_instance_name = instance_name
                break

        if matched_instance_name:
            skip_next_lines = 3
            instance_names.remove(matched_instance_name)
        else:
            new_ssh_config_lines.append(line)

    with open(Config.SSH_CONFIG_PATH, 'w') as ssh_config_file:
        ssh_config_file.writelines(new_ssh_config_lines)
