# Ansible Configurations

This repo is an example of using Ansible to manage multiple data center domains.

There are examples for ACI, NXOS, and UCS. Each example provides a check/monitor and a create/update/remove component to the aspect of the domain that is being managed.

* Technology stack: The primary technology is Ansible, with modules that are available as part of Ansible core and modules that are open sourced.

Additionally there is python code for a simple Flask based webservice that listens for a payload from Github, that is sent on a **push** event.

* Status:  This is Beta code that will change as additional configurations and checks are added to the repository.

## Walk, Run, Fly


### Walk

Use the check.yml files in each domain to check for the specific configuration status. For example VLANs configured on UCS and NXOS and a tenant configured on ACI.

### Run

Use the site.yml files in each domain to add/update/remove the specific configurations in each domain. For example add/update/delete VLANs on UCS and NXOS and a tenant on ACI.

### Fly

Enable the Flask based weblistener to process the payload from a Github push event webhook. Additionally the Flask weblistener can send the results of the push event processing to a Webex Teams room.

## Installation

- Ansible is required, Version 2.7.10 was used when developing this repository
- Create a Python3 virtual environment
- Activate the virtual environment
- Pip install
  - ucsmsdk to enable Ansible to interact with UCS Manager
  - webexteamssdk
  - Flask

## Configuration

- Ansible Vault is used to maintain secrets
- Knowledge of how to use Webex API is required for webhook listener

## Usage

To run an ansible playbook use the following command line in the appropriate domain directory.

`ansible-playbook -i inventory site.yml --vault-password-file=~/.vault_pass.txt`

Because ansible-vault is used the vault password is required to run the playbook in an automated fashion.
