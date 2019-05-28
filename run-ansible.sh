
#!/bin/bash

#### Written by: John McDonough - movinalot
#### Description: Runs Ansible update based on updated site.yml

#### This script is triggered by github push, pull the repo
cd ~/projects/ansible-configurations
git pull

#### Cycle through cmdline parameters, each one represents an Ansible
#### configuration directory. A parameter representing a configuration
#### will only be passed to this script if an update was detected to
#### files in it's directory.

for DOMAIN in "$@"
do
  echo "Processing site.yml for domain: " ${DOMAIN}
  cd ${DOMAIN}
  ansible-playbook -i inventory site.yml --vault-password-file=~/.vault_pass.txt

  if [[ -e site.retry ]]; then
    rm site.retry
  fi
  
  cd ..
done

