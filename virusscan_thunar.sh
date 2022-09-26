#!/bin/bash
# clamscan helper for thunar contextmenue
# should also work for nemo (copy to ~/.local/nemo/scripts)
# 2022 by rundekugel-github

text2=$(clamscan -o $*)
if [ $? != 0 ] 
then
  type=warning
else
  type=info
fi

zenity --$type --title="scan result" --text="$text2" 
