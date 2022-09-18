#!/usr/bin/python3
"""
use to remote control volume and brightness for notebook monitors
use http call android app 'HTTP Shortcuts' or http-bookmarks

 http://<ip-address>:9933/volp=33    ==> set volume to 33%
 http://<ip-address>:9933/bright=63  ==> set brightness of integrated monitor to 63%
 http://<ip-address>:9933/space!     ==> send a space key stroke
 http://<ip-address>:9933/close!     ==> close this

call this script with param -p=<port-number> to listen on different port. or put it in crontab.
"""

import sys, os
print(sys.version)
import socketserver
import time
import subprocess

__author__ = "lifesim.de"
__version__= "1.1.0"


class globs:
  verbose=2
  doit=1
  sock=None
  port = 9933
  #volMax = 65536
  brightMax = 2000
  log=None

class handler(socketserver.BaseRequestHandler):
  def handle(self):
    r="-"
    self.data = self.request.recv(1024).strip()
    if globs.verbose:
      print(self.data)
    if b"close!" in self.data:
      """todo: kill programm softly"""
      globs.doit = 0
      logit("close...", stdout=1)
      globs.sock.server_close()
      time.sleep(1)
      print(".")
      sys.exit(0)
    if b"volp=" in self.data:
      v=self.data.split(b"=")[1].split(b" ")[0].decode()
      v=int(v)
      print("set vol:"+str(v))
      # amixer needs XDG_RUNTIME_DIR set
      cmd = "export XDG_RUNTIME_DIR=/run/user/1000; /usr/bin/amixer -D pulse sset Master "+str(v)+"%"
      r=getShell(cmd)
      #r=os.system(cmd) # used for debug
      logit("vol:"+str(v)+";"+str(r))
    if b"bright=" in self.data:
      v=self.data.split(b"=")[1].split(b" ")[0].decode()
      v=int(v)
      print("set brightness:"+str(v))
      v=int(globs.brightMax *v/100)
      r=os.system("echo "+str(v)+" > /sys/class/backlight/intel_backlight/brightness")
      logit("brightness:"+str(v)+";"+str(r))
    if b"space!" in self.data:
      r=os.system("xdotool key space")
      logit("space:"+str(r), stdout=1)
    try:
      if 0:
        self.request.sendall(b"HTTP/1.1 200 OK\r\n"+
          "Content-Length: 3\r\n" +
          "Content-Type: text/plain\r\n" +
          "Connection: close\r\n" +
          "\r\n"
          +"ok.\r\n"
          )
      else:
        self.request.sendall(f"ok.{r}.\r\n".encode())
    except:
      pass

def logit(text, newline=True, stdout=False):
  if stdout:
    print(text)
  if globs.log:
    if newline:
      text = str(text) +os.linesep
    with open(globs.log, 'a') as f:
      f.write(text)

def setupEnv():
  print("setup env vars...")
  r=os.system("export XDG_RUNTIME_DIR=/run/user/1000") 
  es = ""
  for i in os.environ:
    es += i+"="+os.environ[i] +os.linesep
  logit("env:")
  logit(es)

def getShell(cmd):
  f= os.popen(cmd)
  r=f.read()
  f.close()
  return r

def checkAlreadyRunning():
  # check if a proc with same name already runs
  n = sys.argv[0]
  n=os.path.basename(n)
  cmd = "ps -e |grep "+n[:-1] # we don' wont pid from own shell cmd
  l= getShell(cmd).split(n)
  if len(l)>1: # 2 running
    return True
  return False

# ----------    
def main():
  for p in sys.argv:
    p0,p1=p,""
    if "=" in p: 
      p0,p1=p.split("=",1)
    if p0=="-p": globs.port = int(p1)
    if p0=="-bm": globs.brightMax = int(p1)
    #if p0=="-vm": globs.volMax = int(p1)
    if p0=="-log": globs.log = p1
    
  setupEnv()
  s=0
  if 0: # checkAlreadyRunning():
    logit("There is already an instance running.", stdout=1)
    return
  logit("listen on port "+str(globs.port)+"...", stdout=1)
  try:
    s=socketserver.TCPServer(("0.0.0.0",globs.port), handler)
    globs.sock=s
    s.socket.setsockopt( socketserver.socket.SOL_SOCKET,
                       socketserver.socket.SO_REUSEADDR, 1 )
    s.serve_forever()
  except Exception as e:
    logit(e)
    globs.doit=0
  # logit("serve...", stdout=1)
  while globs.doit:
    time.sleep(1)
  if s: s.server_close()
  logit("done.", stdout=1)

if __name__ == "__main__":
  main()
  
