#!/bin/bash
virtualenv .venv
pip install -r requirements.txt
ansible-galaxy collection install community.general
ansible-galaxy collection install amazon.aws
