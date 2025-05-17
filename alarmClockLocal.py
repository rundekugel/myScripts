#!/usr/bin/env python3

"""
alarmclock depending on environment read from ip-address
by gaul1-lifesim.de
usage:
  weckerLoc.pyw [params]
  
  params:
  -h                help
  -ip=<ipaddress>   add a ipaddress to whitelist
  -i=0|1            icon in taskbar
  -w=0|1            window invisible
  -a=<HH:MM> or <HH:MM:SS>  alarm time
  -m=<message>      alarm message

"""
import os
import socket
from tkinter import messagebox
import tkinter
import time
import sys
import subprocess

__version__ = "1.0.0"

class horm:
  """global values, like hormones"""
  ipwhitelist = ("192.168.177.",)  # alarm only if one of these ips on this machine
  alarmTime = "22:05"  # HH:MM /24 or HH:MM:SS
  # alarmTime = "16:05"  # HH:MM /24 or HH:MM:SS
  message = "Kids abholen"
  snoozeseconds = 200
  doiconify = 1
  doWithdraw = 0
  interval = .5
  
def getIps():
  ips = socket.gethostbyname_ex(socket.gethostname())[2]
  return ips

def fitEnvironment():
  ips = getIps()
  fit = 0
  for ip in ips:
    for w in horm.ipwhitelist:
      if w in ip:
        return True
  return False

def doAlarm(msg="Termin"):
  return messagebox.askretrycancel("Erinnerung!",msg +"\r\n\r\nNochmal in 5min erinnern?")

def getTime(digits=4):
  # digits = len(horm.alarmTime.replace(":",""))
  # if digits >= 6:
  return time.strftime("%H:%M:%S", time.localtime())
  # return time.strftime("%H:%M", time.localtime())

def getHorm():
  msg ="\r\n"
  for k in horm.__dict__:
    if k[0] != "_": msg += k + " = " + str(horm.__dict__[k]) + os.linesep
  return msg

def printHelp():
    msg =__doc__
    msg+= "\r\ndefault settings:\r\n"
    msg += getHorm()
    messagebox.showinfo("Help Message", msg)
    sys.exit()

def guicb():
  txt = horm._txt["text"]
  r = inputBox("Change Value","Enter name=value","alarmTime="+horm.alarmTime)
  if "=" in r:
    k,v = r.split("=",1)
    r = messagebox.askyesno("New Value","Write value "+str(v)+" to "+str(k)+ "?")
    if r:
      ks = ("ipwhitelist", "alarmTime", "message", "snoozeseconds", "doiconify", "doWithdraw")
      ky = (horm.ipwhitelist, horm.alarmTime, horm.message, horm.snoozeseconds, horm.doiconify, horm.doWithdraw)
      if k== "message": horm.message = v
      elif k== "snoozeseconds": horm.snoozeseconds = int(v)
      elif k== "alarmTime": horm.alarmTime = v
  horm._guiText.set(getHorm())

class inputBox(object):
  retval = None
  default = None

  def __new__(cls, title="Input", message="Input:",default=""):
    """this is static class object of inputBox"""
    cls = super(inputBox,cls).__new__(cls)
    g2 = tkinter.Tk()
    g2.title(title)
    cls.default = default
    l = tkinter.Label(g2, text=message,justify=tkinter.LEFT)
    cls.entry = tkinter.Entry(g2)
    cls.entry.insert(0,str(default))
    l.pack(padx=5)
    cls.entry.pack(padx=5)
    tkinter.Button(g2, text="Ok", command=cls.bok).pack(side=tkinter.LEFT, padx=5, pady=5)
    tkinter.Button(g2, text="Cancel", command=cls.bCancel).pack(padx=5,pady=5)  #side=tkinter.LEFT
    cls.retval = None   # has to be set here, because this can be old. there is no new instance
    while cls.retval is None:
      g2.update()
      time.sleep(.1)
    g2.destroy()
    return cls.retval

  def bok(self=None):
    # if self is None: self = inputBox
    self.retval = self.entry.get()
    return self.bok

  def bCancel(self=None):
    # if self is None: self = inputBox
    self.retval = None


def main():
  """the main loop, waiting for alarmTime"""
  doit = True
  happened = 0
  redoTime = None
  r=inputBox(default="asdf")
  gui = tkinter.Tk()
  gui.resizable=(True,True)
  horm._gui = gui
  gui.title("AlarmClock "+horm.alarmTime)
  horm._guiText = tkinter.StringVar()
  horm._guiText.set(getHorm())
  horm._la1 = tkinter.Label(gui, textvariable = horm._guiText, justify=tkinter.LEFT)
  horm._la1.pack(padx=5 )
  btnSettings = tkinter.Button(gui, text="Settings", command=guicb).pack(side=tkinter.BOTTOM,pady=5)
  #   horm._txt = tkinter.Entry(gui, width=30, height=2, text="lkj")
  horm._txt = tkinter.Entry(gui, width=30,  text="lkj")
  horm._txt.pack()
  gui.update()
  if horm.doWithdraw:  gui.withdraw()
  if horm.doiconify:  gui.iconify()
  
  while doit:
    try:
        gui.update()
        gui.update_idletasks()
    except:
      doit = False
      gui = None
    if redoTime and redoTime <= getTime():
      happened = 0
    if getTime() < horm.alarmTime:
      time.sleep(horm.interval)
      happened = 0
      continue
    if happened:
      time.sleep(horm.interval)
      continue
    if fitEnvironment():
      if doAlarm(horm.message):
        redoTime = time.strftime("%H:%M:%S", time.localtime(time.time()+horm.snoozeseconds))
      else: redoTime = None
      happened = 1
    else: time.sleep(horm.interval)
  if gui:  gui.destroy()
  return
  
if __name__ == "__main__":
  for p in sys.argv:
    if "-i=" in p:  horm.iconify=int(p[3:])
    if "-w=" in p:  horm.withdraw=int(p[3:])
    if "-a=" in p:  horm.alarmTime=p[3:]
    if "-m=" in p:  horm.message=p[3:]
    if "-ip=" in p:  horm.ipwhitelist += (p[3:],)
    if "-h" in p:  printHelp()
  main()

#eof
