#!/usr/bin/env python3

"""
use in thunar actions for diff 2 files in different folders
action1: contextDiff.py 1 %F
action2: contextDiff.py 2 %F
"""

import os
import sys
try: 
	from plyer import notification
except:
	notification=None

tmpfile = "/tmp/contextDifftmpdifA"
debug =0

if debug:
   f=open("/home/beb/bin/tmpdif1","w")
   f.write(str(sys.argv))
   f.close()

if sys.argv[1]=="1":
   with open(tmpfile,"w") as f:
      f.write(str(sys.argv[2]))
   if notification:
	   notification.notify("Noted for diff", "Select 2nd file with 'diff2' to diff with "+
		os.linesep+sys.argv[2],timeout=5,app_icon="gnome-session-switch") 

def main():
   if sys.argv[1]=="2":
      fn1 = None
      if len(sys.argv) >3:
          os.popen("meld "+sys.argv[2]+" "+sys.argv[3])
          return
      if not os.path.exists(tmpfile):
         return
      fn2 = sys.argv[2]
      with open(tmpfile,"r") as f:
       fn1 = f.read()
      os.popen("rm "+ tmpfile)
      if fn1:
       os.popen("meld "+fn1+" "+fn2)

main()

#eof
