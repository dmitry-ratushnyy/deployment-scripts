#!/usr/bin/env python3

import json
import subprocess
from config import Config


def main():
    result = subprocess.run(
        ["ansible-inventory", "-i", Config.INVENTORY_PATH, "--list"],
        stdout=subprocess.PIPE,
        text=True,
        check=True
    )

    inventory_data = json.loads(result.stdout)

    filtered_data = {
        "all": {
            "hosts": []
        }
    }

    for _, host_vars in inventory_data["_meta"]["hostvars"].items():
        instance_name = host_vars.get("tags", {}).get("Name", "N/A")

        filtered_host = {
            "instance_name": instance_name,
            "public_ip": host_vars["public_ip_address"],
            "public_dns": host_vars["public_dns_name"]
        }
        filtered_data["all"]["hosts"].append(filtered_host)

    print(json.dumps(filtered_data, indent=2))


if __name__ == "__main__":
    main()
