#!/bin/bash

$(ansible-vault view webhook_vars.yml --vault-password-file ~/.vault_pass.txt)
. ../venv/bin/activate
python webhook_listener.py