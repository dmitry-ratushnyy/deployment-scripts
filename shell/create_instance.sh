#!/bin/bash

SUBSTRATE='k8s'
JUJU_VERSION=3.1
EXTRA_VARS="substrate=$SUBSTRATE juju_version=$JUJU_VERSION"
ANSIBLE_FOLDER="./ansible"

ansible-playbook "${ANSIBLE_FOLDER}/playbooks/create_instance.yml" --extra-vars "$EXTRA_VARS"


echo "Updating ssh config"
python ./python/update_ssh_config.py