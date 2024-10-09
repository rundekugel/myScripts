#!/bin/bash

# works also, if clipman already started

~/cmd/start.sh xfce4-clipman-history
sleep .5 
wmctrl -a "Clipman History" -b add,above 
