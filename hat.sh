#!/usr/bin/env bash
#thanks to: https://stackoverflow.com/users/26510/brad-parks
# enhanced by lifesim.de
nhead=10
ntail=10
if [ "$1" != "" ] ;then
   nhead=$1
fi
if [ "$2" != "" ] ;then
   ntail=$2
fi

IT=$(cat /dev/stdin)
echo "$IT" | head -n$nhead
echo "..."
echo "$IT" | tail -n$ntail

#eof
