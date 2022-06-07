#!/usr/bin/python3
"""
use to remote control volume and brightness for notebook monitors
use http call android app 'HTTP Shortcuts' or http-bookmarks

 http://<ip-address>:9933/volp=33    ==> set volume to 33%
 http://<ip-address>:9933/bright=63    ==> set brightness of integrated monitor to 63%

call this script with param -p=<port-number> to listen on different port.
"""

import sys, os
print(sys.version)
import socketserver
import time
import subprocess

__author__ = "lifesim.de"
__version__= "1.0.2"


class globs:
  verbose=2
  doit=1
  sock=None
  port = 9933
  #volMax = 65536
  brightMax = 2000

class handler(socketserver.BaseRequestHandler):
  def handle(self):
    r="-"
    self.data = self.request.recv(1024).strip()
    if globs.verbose:
      print(self.data)
    if b"close!" in self.data:
      """todo: kill programm softly"""
      globs.doit = 0
      print("close...")
      globs.sock.server_close()
      time.sleep(1)
      print(".")
      sys.exit(0)
    if b"volp=" in self.data:
      v=self.data.split(b"=")[1].split(b" ")[0].decode()
      v=int(v)
      print("set vol:"+str(v))
      r=os.system("/usr/bin/amixer -D pulse sset Master "+str(v)+"%")
    if b"bright=" in self.data:
      v=self.data.split(b"=")[1].split(b" ")[0].decode()
      v=int(v)
      print("set brightness:"+str(v))
      v=int(globs.brightMax *v/100)
      r=os.system("echo "+str(v)+" > /sys/class/backlight/intel_backlight/brightness")
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

def getMaxBrightness():
  v=None
  with open("/sys/class/backlight/intel_backlight/max_brightness",'r') as f:
    v = f.read()
  return int(v)

# ----------    
def main():
  v = getMaxBrightness()
  if v: globs.brightMax = v
  for p in sys.argv:
    p0,p1=p,""
    if "=" in p: 
      p0,p1=p.split("=",1)
    if p0=="-p": globs.port = int(p1)
    if p0=="-bm": globs.brightMax = int(p1)
    #if p0=="-vm": globs.volMax = int(p1)
    
  print("listen on port "+str(globs.port))  
  s=socketserver.TCPServer(("0.0.0.0",globs.port), handler)
  globs.sock=s
  s.socket.setsockopt( socketserver.socket.SOL_SOCKET, 
                     socketserver.socket.SO_REUSEADDR, 1 )  
  s.serve_forever()
  print("n serve")
  while doit:
    time.sleep(1)
  s.server_close()
  print("done.")

if __name__ == "__main__":
  main()
  
