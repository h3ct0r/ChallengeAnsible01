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
- run `ansible-playbook -s -v python2.yml` to install python2.7
- run `ansible-playbook -s -v nodejs_latest.yml` to install the latest nodejs
- create the node app in anoter Git project (https://github.com/h3ct0r/ChallengeNodeApp01)
- modify the project to allow use of several cores with the `cluster` module
- create a tag on the node project
- Add the tag to the git config on the play (node_app.yml)
- Configure play to use `pm2` as deploy tool of the node app, using `-i max` as a load balancer
- Test play with version=2.0.0 now
- To change revisions of the app only need to change version parameter now. (playing with 1.0.0 and 2.0.0)
- Generated TSL keys for HTTPS:
	`openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
        -subj /CN=localhost \
        -keyout files/nginx.key -out files/nginx.crt`
- 