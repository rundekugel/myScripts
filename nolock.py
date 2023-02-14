#!/usr/bin/env python

"""don't lock the screen, if in virtual box"""

import os,sys
import time
import subprocess as sp

class globs:
  doit = 1

def keystroke():
  logit("ks.")
  os.system("C:\\work\\myScripts\\myScripts\\nlock.vbs")

def isVM():
   logit("isv")
   r=sp.check_output("cmd /c wmic diskdrive get model")
   logit(r)
   return "VBOX " in r

def logit(text):
  try:
    f=open("C:\\work\\myScripts\\myScripts\\nolock.log","a")
    f.write(text+os.linesep)
    f.close
  except:
    pass

def main():
  globs.doit = 1
  logit("start")
  while globs.doit:
    time.sleep(10)
    if isVM():
      keystroke()


main()



