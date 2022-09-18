#!/usr/bin/env python3

"""
use in thunar actions for copy path to clipboard
"""


import sys
import pyperclip
from plyer import notification

path=sys.argv[1:]
if len(path)>1:
	path=str(path)
else:
	path=path[0]
notification.notify("Copy Path to Clipboard", path)
pyperclip.copy(path)

#eof
