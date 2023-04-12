#!/usr/bin/env python
"""
create a mime-type from file-extension for xfce-desktop to tell thunar to open it with a
desired application

params:
-e=<fileextension>   the fileextension which shall be opened
-t=<filetype>        new name for a filetype
-p=<vendor-prefix>   default=extension
-f=<0|1>             force overwriting existing files. Be careful!
-c=<comment>         optional explanation of new filetype.

"""
# -a=<full application path>  application to open the files with the specific extension

"""
debug info:
~/.config/mimeapps.list
text/x-myvendor-mytype=myapplication.desktop
~/.local/share/applications
"""



import sys,os

__version__="0.0.1"
__revision__="0"


class globs:
   verbosity=1

   
def dofiles(fileextension=None, vendor="ano", filetype=None, comment="", 
            apppath=None, force=0):
   if not filetype:
      raise Exception("Filetype must be set!")
   if not fileextension:
      raise Exception("Fileextension must be set!")
   while fileextension[0]==".":
      fileextension=fileextension[1:]
   # fn = "/usr/share/mime/packages/" + vendor +"-"+ filetype +".xml"
   fn = "/tmp/" + vendor +"-"+ filetype +".xml"
   if not force and os.path.isfile(fn):
      raise Exception(f"File {fn} exists, already!")
   if globs.verbosity:
      print(f"create file: {fn}...")
   with open(fn,"w") as f:
      f.write( f"""<?xml version="1.0" encoding="utf-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
 <mime-type type="application/x-{vendor}-{filetype}">
  <comment>{comment}</comment>
  <glob weight="60" pattern="*.{fileextension}"/>
</mime-type>
</mime-info>
      """)
   os.popen("xdg-mime install "+ fn)
"""
~/.config/mimeapps.list
text/x-segger-ozone=ozone.desktop
"""
      
      
   
def main():
   fileextension=None
   vendor="extension"
   filetype=None
   apppath=None   
   comment=""
   force = False
   
   if 1:
      fileextension=".test3"
      filetype="mytype3"
      apppath="~/prg/t/exe3.sh"
      comment="my test-type-3"
      force=1
   
   print("create a mime-type from file-extension for xfce-desktop")
   
   for arg in sys.argv[1:]:
      p = arg.split("=", 1);
      p1 = ""
      if len(p) > 1: p1 = p[1]
      p=p[0]
      if p in ("-h", "?", "--help", "-?"):
        print("createXfceMimeType " + __version__ + "." + __revision__)
        print(__doc__)
        sys.exit(0)
      if p == "-e": fileextension = p1
      if p == "-p": vendor = p1
      if p == "-t": filetype = p1
      if p == "-f": force = int(p1)
      if p == "-a": apppath = p11
      if p == "-c": comment = p1
      if p == "-v": globs.verbosity = int(p1)
      if p == "-V": print("Version: " + __version__ + "." + __revision__)
      
   return dofiles(fileextension, vendor, filetype, comment, apppath, force)

if __name__ == "__main__":
   sys.exit(main())
   
#eof
   
