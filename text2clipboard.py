#!/usr/bin/env python3

"""
use in thunar actions for copy path to clipboard
similar to xclip, but with gui notification
"""


import sys,os
import pyperclip
from plyer import notification

path=sys.argv[1:]
path=os.linesep.join(path).strip()
notification.notify("Copy Path to Clipboard", path)
pyperclip.copy(path)

#eof
