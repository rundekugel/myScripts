#!/bin/bash
# by rundekugel-lifesim.de 
text=$(git log --date=iso  -n 1  --format=format:"Date: %ad%nHash: %h%n")
text2=$text"\n"$(git remote -v)
text2=$text2"\n\nby rundekugel-lifesim.de"
# echo $text2
zenity --info --title="GIT infos" --text="$text2" 

