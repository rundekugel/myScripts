#!/bin/bash

read -p "taskname: " prg
# prg=$1 # this doesn't work, 'cause it'll be found in tasklisk
if [ "$prg" == "" ];then
  echo usage: $0 \<taskname\> \(optional with parameters\)
  echo you\'ll be notified, if task is finished
  exit
fi 

d=1
while [ $d == 1 ]
do 
 echo test for $prg
 sleep 1
 r=$(ps -A x)
 echo $r|grep "$prg" >/dev/null
 if [ $? != 0 ];then  
   echo task gone: $r|grep "$prg"
   d=0
 fi
done
notify-send $1 finished.
#eof

