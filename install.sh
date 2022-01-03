#!/bin/bash

mkdir -p $HOME/.anacron/etc/ $HOME/.anacron/var/spool
touch $HOME/.anacron/etc/anacrontab

echo "SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
HOME=$HOME
LOGNAME=$USER

#period delay   job_identifier  command
7       0   arxivnotif.weekly     cd $PWD && python3 arxivnotif.py" > $HOME/.anacron/etc/anacrontab
