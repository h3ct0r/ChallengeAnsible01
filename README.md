# ChallengeAnsible01

Running this challenge on MacOS, with the help of: Ansible Up & Running (Lorin Hochstein) and Ansible for DevOps (Jeff Geerling).

## First steps:

- Install brew if not already installed
- `brew install ansible`

## And then:

- create a `playbook` folder to store your playbooks
- add your hosts domains/ip to a `hosts` file
- create a `ansible.cfg` to automate some basic configs to the hosts
- test if we reach the new host
	`ansible challengeserver -m ping`
- server reached but remote server shows error '"/bin/sh: 1: /usr/bin/python: not found\r\n"', so we need to install python2.7