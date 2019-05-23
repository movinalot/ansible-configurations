
#!/bin/bash

#### Written by: John McDonough - movinalot
#### Description: Runs Ansible update based on updated site.yml

#### This script is triggered by github push, pull the repo
cd ~/projects/ansible-configurations
git pull

#### Retrive enviroment variables that are needed for NXOS Ansible
$(ansible-vault view env_vars.yml --vault-password-file ~/.vault_pass.txt)

#### Cycle through cmdline parameters, each one represents an Ansible
#### configuration. A parameter representing an Ansible configuration
#### will only be passed to this script if an update was detected to
#### its' site.yml
####

for DOMAIN in "$@"
do
  echo ${DOMAIN}
  cd ${DOMAIN}
  ansible-playbook -i inventory site.yml
  cd ..
done

#### unset NXOS authentication environment variables
unset ANSIBLE_NET_USERNAME
unset ANSIBLE_NET_PASSWORD
