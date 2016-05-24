#!/usr/bin/env bash

TARGETWORD="requiretty"

NEWWORD="\!requiretty"

TARGETTEXT="/etc/sudoers"
BACKUP="backup"
TEMPFILE="/tmp/out.tmp"

[ ! -d $BACKUP ] && mkdir -p $BACKUP || :


if [ -f $TARGETTEXT ]; then

	FOUND=`grep "$NEWWORD" $TARGETTEXT`

	if [ ! -n "$FOUND" ]; then 

		/bin/cp -f $TARGETTEXT $BACKUP

		sed "s/$TARGETWORD/$NEWWORD/" "$TARGETTEXT" > $TEMPFILE 

		echo "sysdev  ALL=(ALL)       ALL # added sysdev" >> $TEMPFILE 
		echo "sysdev  ALL=NOPASSWD: /usr/bin/systemctl, /var/www/voltage-ent.com/witches-server/*" >> $TEMPFILE

		mv $TEMPFILE "$TARGETTEXT"

	else
		echo "Already Modified"

	fi
else
	echo "no sudoers found"
	exit 1

fi