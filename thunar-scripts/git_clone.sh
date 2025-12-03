#!/bin/bash
# by rundekugel-lifesim.de 
echo try git clone to $1...
cd $1
url=$(zenity --entry --text "Enter git url" --title "Git clone")
git clone $url
sleep 2

