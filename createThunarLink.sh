#!/bin/bash
here=$(pwd)
tnam=$(basename $1)
name=$here/linkTo_$tnam.sh
echo name: $name
echo "#!/bin/bash" > $name
echo thunar $1 \& >> $name
chmod +x $name
