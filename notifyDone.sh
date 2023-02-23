#!/bin/bash

prg=$1
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
 echo $r|grep $1 >/dev/null
 if [ $? != 0 ];then  
   echo $r|grep $1
   d=0
 fi
done
notify-send $1 finished.
#eof

