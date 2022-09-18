#!/bin/bash
# by lifesim.de
# start a file, only once.

MYDIR=$(cd $(dirname "$0"); pwd)
userid=$(id -u)

if [ -$1- == -- ];then
me=$(basename $0)
# usage 
echo usage: $me <app> [name]
exit 1
fi
name=$2
if [ -$name-  == -- ];then
name=$(basename $1)
fi
#pidfile=/var/run/$2.pid
pidfile=/tmp/lock-$userid-$name

if [ -e $pidfile ]; then
pid=`cat $pidfile`
if kill -0 &>1 > /dev/null $pid; then
echo "Already running"
exit 1
else
rm $pidfile
fi
fi
if ! echo $$ > $pidfile ; then
echo pidfile creation failed "$pidfile"
fi
#do your thing here
$*
sleep 1

rm $pidfile
