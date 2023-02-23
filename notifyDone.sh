#!/bin/bash

read -p "taskname: " prg
# prg=$1 # this doesn't work, 'cause it'll be found in tasklisk
if [ "$prg" == "" ];then
  echo usage: $0 \<taskname\> \(optional with parameters\)
  echo you\'ll be notified, if task is finished
  exit
fi 

d=1
while [ $d != 0 ]
do 
 echo -en wait, while process \"$prg\" running... $d sec.\\r
 d=$((d+1))
 sleep 1
 r=$(ps -A x)
 echo $r|grep "$prg" >/dev/null
 if [ $? != 0 ];then  
   d=0
 fi
done
echo -e process \"$prg\" gone.
notify-send "process \"$prg\" gone."
#eof

