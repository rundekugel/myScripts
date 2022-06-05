#!/usr/bin/python3.9
"""
use to remote control volume and brightness for notebook monitors
use http call android app 'HTTP Shortcuts' or http-bookmarks

 http://<ip-address>:8888/volp=33    ==> set volume to 33%
 http://<ip-address>:8888/bright=63    ==> set volume to 63%

call this script with param -p=<port-number> to listen on different port.
"""

import sys, os
print(sys.version)
import socketserver
import time
import subprocess

__author__ = "lifesim.de"
__version__= "1.0"

class globs:
  verbose=2
  doit=1
  sock=None
  port = 8888
  #volMax = 65536
  brightMax = 2000

class handler(socketserver.BaseRequestHandler):
  def handle(self):
    self.data = self.request.recv(1024).strip()
    if globs.verbose:
      print(self.data)
    try:
      if 0:
        self.request.sendall(b"HTTP/1.1 200 OK\r\n"+
          "Content-Length: 3\r\n" +
          "Content-Type: text/plain\r\n" +
          "Connection: close\r\n" +
          "\r\n"
          +"nok.\r\n"
          )
      else:
        self.request.sendall(b"ok.\r\n")
    except:
      pass
    if b"close!" in self.data:
      """todo: kill programm"""
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
      os.system("/usr/bin/env amixer -D pulse sset Master "+str(v)+"%")
    if b"bright=" in self.data:
      v=self.data.split(b"=")[1].split(b" ")[0].decode()
      v=int(v)
      print("set brightness:"+str(v))
      v=int(globs.brightMax *v/100)
      os.system("echo "+str(v)+" > /sys/class/backlight/intel_backlight/brightness")


def main():
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
  
