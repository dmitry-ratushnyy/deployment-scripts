#!/usr/bin/env python3

import json
import subprocess
import os
from utils import update_ssh_config

INVENTORY_PATH = os.path.abspath('./ansible/inventory_aws_ec2.yml')


def main():
    inventory_data = get_inventory_data()
    filtered_data = filter_inventory_data(inventory_data)
    update_ssh_config(filtered_data)
    print(json.dumps(filtered_data, indent=2))


def get_inventory_data():
    result = subprocess.run(
        ["ansible-inventory", "-i", INVENTORY_PATH, "--list"],
        stdout=subprocess.PIPE,
        text=True,
        check=True
    )

    return json.loads(result.stdout)


def filter_inventory_data(inventory_data):
    filtered_data = {
        "all": {
            "hosts": []
        }
    }

    for host, host_vars in inventory_data["_meta"]["hostvars"].items():
        instance_name = host_vars["tags"]["Name"] if "Name" in host_vars["tags"] else "N/A"
        filtered_host = {
            "instance_name": instance_name,
            "public_ip": host_vars["public_ip_address"],
            "public_dns": host_vars["public_dns_name"]
        }
        filtered_data["all"]["hosts"].append(filtered_host)

    return filtered_data


if __name__ == "__main__":
    main()
