#!/bin/bash
# by rundekugel-lifesim.de 
# show pupup with git repo infos. add to thunar for your comfort.
text=$(git log --date=iso  -n 1  --format=format:"Date: %ad%nHash: %h%n")
text2=$text"\n"$(git remote -v)
# echo $text2
zenity --info --text="$text2"
