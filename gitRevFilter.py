#!/usr/bin/env python
"""
replace tags when git commit or git checkout
this file must be in executable path
usage: gitRevFilter install [-global] -f=<filefilter> [-n=<filtername>]
 -global doesn't work yet
 -f=filefilter: i.e. *.c, *.txt,*.py,... may be commaseperated, but no spaces
 -n=filtername: a new git filter name as text
 -c=only for clean (not implemented yet)
 -s=only for smudge (not implemented yet)
 -dp=n  debuug port. 0=disabled (default)
 -V  version
 -v=0..n verbosity
"""

import sys, os
import socket
import subprocess as sp
import time

__version__ = "0.2"
__revision__ = "$Rev: dcbd19f $"[6:-2]
__author__ = "gaul1 - at - lifesim.de"


class globs:
  debugport = 0
  verbosity = 0


def xchangeTag(tag, line, text):
  """
   tag without $$, line to xchange, new text inside tag
   """
  ll = line.split("$" + tag)
  nl = ll[0]
  for l in ll[1:]:
    if not "$" in l:
      return line
    l = l.split("$", 1)[1]
    nl += "$" + tag + ": " + text + " $" + l
  return nl

def tcpTx(text):
  try:
    r = sp.run('git config filter.gitRevFilter.dbgPort'.split(" "), capture_output=True)
    if 0 == r.returncode:
      globs.debugport = int(r.stdout)
    if globs.debugport:
      if globs.verbosity > 3:
        print("Debugport:" + str(globs.debugport))
      serv = ("127.0.0.1", globs.debugport)
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect(serv)
      s.send(b"----:")
      loginfo = text + os.linesep
      s.send(loginfo.encode())
      time.sleep(.1)
      s.close()
  except:
    pass

def doit():
  hash = ""
  newDate = ""
  loginfo = ""
  tcpTx("test1")
  r = sp.run('git log --date=iso -n 1 --format=format:%ad;%h'.split(" "), capture_output=True)
  if r.returncode:
    hash = "---";
    newDate = "---"
    al = "error git hash reading" + str(r.stderr)
  else:
    newDate, hash = r.stdout.decode().split(";")
    # hash.replace('"','')

  for line in sys.stdin:
    loginfo += line
    # for tag in ("Rev","Date"):
    if "      line = xchangeTag("Rev", line, hash)
    if "      line = xchangeTag("Date", line, newDate)
    loginfo += line
    sys.stdout.write(line)

  tcpTx(str(loginfo))
  return 0

def install(args):
  if "-global" in args:
    print("install global - not implemented yet")
    return
  me = sys.argv[0]
  filter = []
  myfiltername = "gitRevFilter"
  attr = []
  me=me.replace("\\", "\\\\")
  print("install handler: " + me)
  print("install to this repo path only")
  for arg in args:
    p = arg.split("=", 1);
    p1 = ""
    if len(p) > 1: p1 = p[1]
    p = p[0]
    if p == "-f": filter = p1.split(",")
    if p == "-n": myfiltername = p1
    if p == "-s": attr.append("s")
    if p == "-c": attr.append("c")

  f = open(".gitattributes", "a+")
  for fi in filter:
    f.write(fi.strip() + " filter=" + myfiltername + os.linesep)
  f.close()

  run = "git config filter." + myfiltername + ".clean " + me
  r = sp.run(run.split(" "))
  if r.returncode:
    print("error git config: " + r.stderr)

  run = "git config filter." + myfiltername + ".smudge " + me
  r = sp.run(run.split(" "))
  if globs.debugport:
    run = "git config filter." + myfiltername + ".dbgPort " + str(globs.debugport)
    sp.run(run.split(" "))
  if r.returncode:
    print("error git config: " + r.stderr)
    return r.returncode
  print("done.")
  return 0

def uninstall(args):
  print("uninstall to this repo path only.")
  myfiltername = "gitRevFilter"
  for arg in args:
    p = arg.split("=", 1);
    p1 = ""
    if len(p) > 1: p1 = p[1]
    p = p[0]
    if p == "-n":
      myfiltername = p1

  run = "git config --unset filter." + myfiltername + ".smudge"
  r = sp.run(run.split(" "))
  run = "git config --unset filter." + myfiltername + ".clean"
  r = sp.run(run.split(" "))
  run = "git config --unset filter." + myfiltername + ".dbgPort"
  sp.run(run.split(" "))
  return 0

if __name__ == "__main__":
  a = sys.argv
  tcpTx("t0")
  if len(a) > 1:
    for arg in a[1:]:
      p = arg.split("=", 1);
      p1 = ""
      if len(p) > 1: p1 = p[1]
      p=p[0]
      if p in ("-h", "?", "--help", "-?"):
        print("gitRevisionFilter " + __version__ + "." + __revision__)
        print(__doc__)
        sys.exit(0)
      if p == "-dp": globs.debugport = int(p1)
      if p == "-v": globs.verbosity = int(p1)
      if p == "-V": print("Version: " + __version__ + "." + __revision__)
    if "install".lower() in a[1:]:
      sys.exit(install(sys.argv))
    if "uninstall".lower() in a[1:]:
      sys.exit(uninstall(sys.argv[1:]))
  doit()
# eof
