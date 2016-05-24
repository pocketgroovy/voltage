#!/usr/bin/env bash
set -o errexit

USER_HOST=$1
SSH_KEY=~/.ssh/id_rsa.pub

if [ ! -f $SSH_KEY ]; then
	echo "generate ssh key"
	ssh-keygen -t rsa
fi

if [ ! -z "$USER_HOST" ]; then
	
	if ( ssh $USER_HOST '[ ! -d ~/.ssh ]' ); then
		echo "create .ssh dir in remote system"
		ssh $USER_HOST mkdir -p .ssh
		echo "change permission on .ssh"
		ssh $USER_HOST 'chmod 700 .ssh/'
	fi

	echo "copy public key to remote system"
	cat ~/.ssh/id_rsa.pub | ssh $USER_HOST 'cat >> .ssh/authorized_keys'
	echo "change permission on authorized_keys"
	ssh $USER_HOST 'chmod 640 .ssh/authorized_keys'

	echo "Done. Try ssh in without password"
else
	echo "please enter user@host"
	exit 1
fi

