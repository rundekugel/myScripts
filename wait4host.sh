#!/bin/bash
r=1; while [ $r != 0 ] ; do ping fritz.box -c1 ; r=$?; echo $r; sleep 1; date; done
