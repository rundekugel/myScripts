#!/bin/bash

echo try to set focus to Geany...
wmctrl -a geany
r=$?
if [ $r -eq 0 ] ;then
    exit 0
fi    
echo not found, starting new instance...
geany &
exit 0
