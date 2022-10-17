#!/usr/bin/env python
"""
replace tags when git commit or git checkout
usage: install [-global] -f=<filefilter> [-n=<filtername>]
 -global doesn't work yet
 -f=filefilter: i.e. *.c, *.txt,*.py,... may be commaseperated, but no spaces
 -n=filtername: a new git filter name as text
 -c=only for clean (not implemented yet)
 -s=only for smudge (not implemented yet)
"""

import sys, os
import socket
import subprocess as sp
import time


__version__ = "0.1"
__revision__ = "$Rev:$"[5:-2]
__author__ = "gaul1 - at - lifesim.de"

debug = 1


def xchangeTag(tag,line,text):
   """
   tag without $$, line, new text inside tag
   """
   ll= line.split("$"+tag)
   nl = ll[0]
   for l in ll[1:]:
      if not "$" in l:
         continue
      l=l.split("$",1)[1]
      nl+="$"+tag +": "+text+" $"+l
   return nl   

def doit():
   hash=""
   newDate=""
   loginfo=""
   r = sp.run('git log --date=iso -n 1 --format=format:%ad;%h'.split(" "), capture_output=True)
   if r.returncode:
         hash="---"; newDate="---"
         al = "error git hash reading"+str(r.stderr)
   else:      
      newDate, hash = r.stdout.decode().split(";")
      # hash.replace('"','')
      
   for line in sys.stdin:
     loginfo+=line
     # for tag in ("Rev","Date"):
     if "$Rev" in line:
         line = xchangeTag("Rev", line, hash)
     if "$Date" in line:
         line = xchangeTag("Date", line, newDate)
     loginfo+=line
     sys.stdout.write(line)

   if debug:
      serv = ("127.0.0.1",7777)
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect(serv)
      s.send(b"----:")
      s.send(str(loginfo).encode())
      time.sleep(.1)
      s.close()
   return 0

  
def install(args):
   if "-global" in args:
      print("install global - not implemented yet")
      return
   me = args[0]
   filter=[]
   myfiltername = "gitRevFilter"
   attr=[]
   print(me)
   
   print("install to this repo path only")
   for arg in args:
      p=arg.split("=",1);p1=""
      if len(p)>1: p,p1=p
      if p=="-f": filter = p1.split(",")
      if p=="-n": myfiltername = p1
      if p in ("-h","?","--help", "-?"): 
         print("gitRevisionFilter "+__version__+"."+__revision__)
         print(__doc__)
         return
      if p=="-s": attr.append("s")
      if p=="-c": attr.append("c")

   f = open(".gitattributes","a+")
   for fi in filter:
      f.write(fi + " filter="+myfiltername+os.linesep)
   f.close()
   
   run="git config filter."+myfiltername+".clean "+me
   r=sp.run(run.split(" "))
   if r.returncode:
      print("error git config: "+r.stderr)
 
   run="git config filter."+myfiltername+".smudge "+me
   r=sp.run(run.split(" "))
   if r.returncode:
      print("error git config: "+r.stderr)
      return r.returncode
   print("done.")
   return 0
  
def uninstall(args):
   print("uninstall to this repo path only.")
   for arg in args:
      p=arg.split("=",1);p1=""
      if len(p)>1: p,p1=p
      if p=="-n": myfiltername = p1

   myfiltername = "gitRevFilter"
   run="git config --unset filter."+myfiltername+".smudge"
   r=sp.run(run.split(" "))
   run="git config --unset filter."+myfiltername+".clean"
   r=sp.run(run.split(" "))
   return 0
  
if __name__ == "__main__":
   a=sys.argv
   if len(a)>1:
      if a[1] in ("-h","?","--help", "-?"): 
         print("gitRevisionFilter "+__version__+"."+__revision__)
         print(__doc__)      
         sys.exit(0)
      if "install".lower() in a[1:]:
         sys.exit( install(sys.argv) )
      if "uninstall".lower() in a[1:]:
         sys.exit( uninstall(sys.argv) )
   else:
      doit()
#eof      
