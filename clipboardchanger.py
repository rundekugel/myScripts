#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
"""GUI to manipulate clipboard"""

import time
import os

__revision__ = "$Rev: 3 $"[6:-1]
__version__ = "0.1.1"
__author__ = "lifesim.de"

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


d1={"Du":"du","Euch":"euch", "Dein":"dein","Deiner":"deiner",
  "Ihr":"ihr", "@platzhalter":"neuer Text",
  "Euer":"euer"
    }

verbosity = 0

class seperators:
  space=" "
  noLetter="nl"
  
class Guicb:
    _top = None
    _dict = {}
    seperateBy = []
    letterlist =""
    checkbefore = False # check if the char before the keyword is a letter
    checkafter = True
    
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        rzminmax_support = self
        self.initLetterlist()
        self._dict = d1

        if top:
            _top = top
        else:
            self._top = tk.Tk()
            top = self._top
        top.geometry("300x50+50+50")

        top.resizable(1,  1)
        top.title("Change Clipboard content")

        self.BChange = tk.Button(top)
        self.BChange.place(relx=0.1, rely=0.1, height=24, width=50)
        self.BChange.configure(command=self.doChange)

        self.BChange.configure(text='''Change''')


    def initLetterlist(self):
      ll=""
      for b in range(0,26):
        ll+= chr(65+b) + chr(97+b)
      ll+="äöüÄÖÜëß"
      self.letterlist = ll

    def doChange(self):
      cb=self._top.selection_get(selection="CLIPBOARD")
      if verbosity >2:
        print(cb)
      pos,leng =0, len(cb)
      keys = self._dict.keys()
      changed = 0
      for key in keys:
        pos = 0
        while pos < len(cb):  # leng must be recalculated, if exchange changes length of cb
          r=cb[pos:].find(key)
          pos += r
          if r<0: # not found
            pos = leng #next key
            continue
          if self.checkafter:
            nx= cb[pos+len(key)]
            if nx in self.letterlist:
              pos += len(key)
              continue
          if self.checkbefore:
            if pos>1:
              bf = cb[pos-1]
              if bf in self.letterlist:
                pos += len(key)
                continue
          #xchange:
          left=cb[:pos]
          right=cb[pos+len(key):]
          newword = self._dict[key]
          cb = left + newword + right
          pos += len(newword)
          changed +=1
      if changed:
        self._top.clipboard_clear()
        self._top.clipboard_append(cb)

    def refresh(self):
        """call this repeatedly to update gui"""
        try:
          if self._top.children:
            self._top.update_idletasks()
            self._top.update()
          else:
            return 1
          return 0
        except:
          return 1

def main():
  """run gui"""
  gui = Guicb()
  gui._top.title("Clipbaord Changer V"+str(__version__))+"-"+__revision__

  intervall = .07
  dorun=1
  while(dorun):
    if gui.refresh():
      dorun = 0
      gui = None
      break
    time.sleep(intervall)  
  return

if __name__ == '__main__':
    main()

# eof
