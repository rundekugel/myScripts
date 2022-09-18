#!/usr/bin/env python3

"""
use to change formatted text to plain text
"""

import pyperclip

try: 
	from plyer import notification
except:
	notification=None

t = pyperclip.paste()
pyperclip.copy(t)

if notification:
  notification.notify("Clipboard", "Text plained",
	timeout=5,app_icon="gnome-session-switch") 

#eof
