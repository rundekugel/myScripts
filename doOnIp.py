#!/usr/bin/env python
"""
(C) by rundekugel @github
put this in your autostart folder, helps to start some apps depending on your location.
"""

import sys
import os

#import ipaddress 
import time
import socket
  
class winsize():
  min = "min"
  max = "max"
  normal = "normal"
  
def winstart(cmdline, size=""):
  """
  cmdline to execute in new window
  optional size one of ["min","max","normal"]
  """
  title = cmdline[-8:7]
  size = size.lower()
  param = ""
  if size in ["min","max","normal"]:
    param += " /"+size
  
  cl = 'start "%s" %s %s'%(title, param, cmdline)
  print(cl)
  os.system(cl)
  #os.system('start %s /K %s'%(cmdline))   # for debug only

def main():
  print(sys.version)
  ips = socket.gethostbyname_ex(socket.gethostname())[2]

  print(ips)
  nets = []

  for ip in ips:
    if "172.168." in ip:
      nets.append("office")
    if "10.22.0" in ip:
      nets.append("vpn")
    if "192.168.178." in ip:
      nets.append("home")
    if "192.168.1." in ip:
      nets.append("girlfriend")
    if "10.99." in ip:
      nets.append("train")
      
  print("locations:")
  print(nets)

  if nets and not "office"  in nets:
    print("vpn...")
    winstart('"C:\\Program Files\\OpenVPN\\bin\\openvpn-gui.exe" --connect VPNConfig.ovpn', winsize.min)
    print("time logger...")
    winstart('"C:\\Program Files (x86)\\....exe"')

  if "home" in nets:
    winstart('"C:\\Users\\...\\Music\\radio\\vlc-home.html"')  # controler for external mp3 radio
    winstart('"C:\\Program Files (x86)\\FritzMonitor\\FritzAnrufmonitor.exe ip1"', winsize.min)

  if "girlfriend" in nets:
    winstart('"C:\\Users\\...\\Music\\radio\\vlc-gf.html"')
    winstart("http://homeautomation...")
    winstart('"C:\\Program Files (x86)\\FritzMonitor\\FritzAnrufmonitor.exe ip2"', winsize.min)
    
  ti=15;d=3
  for i in range(ti*d):
    if sys.version_info[0]==3:
      print("closeing in %03.1f sec...\r"%(ti -float(i)/d), end='')
    else:
      print("cloeing in %03.1f sec...\r"%(ti -float(i)/d) ),
    time.sleep(float(1)/d)


if __name__ == "__main__":
  main()
  
#--- eof ---
