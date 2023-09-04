#!/bin/bash

SUBSTRATE='k8s'
JUJU_VERSION='3.1'
EXTRA_VARS="substrate=$SUBSTRATE juju_version=$JUJU_VERSION"
AWS_INSTANCE_KEY_PATH="./aws.pem"
ANSIBLE_FOLDER="./ansible"

ansible-playbook "${ANSIBLE_FOLDER}/playbooks/create_instance.yml" --extra-vars "$EXTRA_VARS"

playbooks=(
  "${ANSIBLE_FOLDER}/playbooks/install_packages.yml"
  "${ANSIBLE_FOLDER}/playbooks/clone_repos.yml"
  "${ANSIBLE_FOLDER}/playbooks/${SUBSTRATE}_juju_${JUJU_VERSION}.yml"
)

for playbook in "${playbooks[@]}"; do
    ansible-playbook "$playbook" -i ${ANSIBLE_FOLDER}/inventory_aws_ec2.yml --extra-vars "$EXTRA_VARS" --private-key $AWS_INSTANCE_KEY_PATH
done

echo "Updating ssh config"
python ./python/update_ssh_config.py