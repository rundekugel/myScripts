#!/bin/sh

r=1
c=1
echo --- start ---
while [ $r != 0 ]
do
echo ---------------------------
echo loop counter: $c
echo executing: $*
$*
r=$?
echo r:$r
c=$(( $c +1 ))
echo ---------------------------
done
echo --- done ---
