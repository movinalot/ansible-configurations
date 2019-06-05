#!/bin/bash

$(ansible-vault view webhook_vars.yml --vault-password-file ~/.vault_pass.txt)

python webhook_listener.py