#!/usr/bin/env python

"""don't lock the screen, if in virtual box"""

import os,sys
import time
import subprocess as sp

class globs:
  doit = 1

def keystroke():
  print("ks.")
  os.system("nlock.vbs")

def isVM():
   r=sp.check_output("cmd /c wmic diskdrive get model")
   return "VBOX " in r

def main():
  globs.doit = 1
  while globs.doit:
    time.sleep(10)
    if isVM:
      keystroke()


main()



