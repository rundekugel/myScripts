#!/usr/bin/env python
"""
create a mime-type from file-extension for xfce-desktop to tell thunar to open it with a
desired application

params:
-a=<application path>  application to open the files with the specific extension
-c=<comment>         optional explanation of new filetype.
-e=<fileextension>   the fileextension which shall be opened
-f=<0|1>             force overwriting existing files. Be careful!
-i                   interactive
-p=<vendor-prefix>   default=ext
-t=<filetype>        new name for a filetype
"""

# todo: -r remove

"""
debug info:
~/.config/mimeapps.list
text/x-myvendor-mytype=myapplication.desktop
~/.local/share/applications
~/.local/share/mime/application/
~/.local/share/mime/packages/
"""

import sys,os

__version__="0.1.0"
__revision__="1"


class globs:
   verbosity=1
   fileextension=None
   vendor="ext"
   filetype=None
   apppath=None
   comment=""
   force = False
   interactive = 0


def registerMimeType(fileextension=None, vendor="extension", filetype=None, comment="",
            apppath=None, force=0):
   """
   write xml-file and register new filetype with file-extension
   :param fileextension: the extension i.e.: .test1
   :param vendor:
   :param filetype: a new name for a filetype
   :param comment: a nice explanation
   :param apppath: not used now
   :param force: 1=overwrite existing file
   :return: 0=ok
   """
   # search for fileext. in xml files first. 
   while fileextension[0] == ".":
      fileextension=fileextension[1:]
   fn = None
   for p in ["~/.local/share/mime/packages/", "/usr/share/mime/packages/"]:
     p=os.path.expanduser(p)  
     for fil in os.listdir(p):  # scan files
       fil = p+os.sep+fil
       if fil.lower()[-4:]==".xml":
         with open(fil,"r") as f:   # search for fileext
           c = f.read()
           if f'"*.{fileextension}"' in c.replace(" ",""):
             # read mimetype from this file out of <mime-type type="application/x-extension-fcstd">
             k = c.split("type=",1)[1:]
             if not k: continue
             c = k[0].split(">")[0]
             if c[-1]=="/": c=c[-1:]
             if not c: continue
             if not force:
               if globs.verbosity:
                 print(f"Filetype {filetype} changed to existing {c}.")
               filetype = c
               fn = fil
             break
   
   if not filetype:
      raise Exception("Filetype must be set!")
   if not fileextension:
      raise Exception("Fileextension must be set!")
   if not fn:
     fn = "/tmp/" + vendor +"-"+ filetype +".xml"
     if globs.verbosity:
       print(f"create file: {fn}...")
     if not force and os.path.isfile(fn):
        raise Exception(f"File {fn} exists, already!")
     with open(fn,"w") as f:
        f.write( f"""<?xml version="1.0" encoding="utf-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
 <mime-type type="application/x-{vendor}-{filetype}">
  <comment>{comment}</comment>
  <glob weight="60" pattern="*.{fileextension}"/>
</mime-type>
</mime-info>
   """)

   # the following line registers mime-type and copies the xml to ~/.local/share/mime/packages/
   return os.popen("xdg-mime install " + fn)._proc.wait()

def modMimelist(apppath, mimetype, comment="",
             force=0):
   """
   modificate the mime-list and register application
   :return: 0=ok
   """
   mlist = os.path.expanduser("~/.config/mimeapps.list")
   # write desktop file
   app = os.path.basename(apppath)
   desktopfn = f"userapp-{app}.desktop"
   with open(os.path.expanduser(
           f"~/.local/share/applications/{desktopfn}")
           ,"w") as f:
      f.write(
      f"""[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
NoDisplay=true
Exec={apppath} %f
Name={app}
Comment={comment}
"""
      )
   with open(mlist,"r") as f:
      mlines = f.readlines()

   ml2 = []
   state = None
   for l in mlines:
      l=l.strip()
      if mimetype in l:
         a,b = l.split("=",1)
         b = ";"+b
         if state == "D":
            b="" # no ';' for [default appl]
            state = "done"
         if not desktopfn in l:
            l=mimetype + "=" + desktopfn + b
         if state == "A": state = "D"
      if l=="[Added Associations]": state="A"
      if l=="[Default Applications]":
         if state !="D":   # not written
            if not ml2[-1]: ml2.pop()   # remove last line, if empty
            ml2.append(mimetype +"="+ desktopfn +";")
            ml2.append("")
         state="D"
      if l=="[Removed Associations]":
         if state !="done":   # not written
            if not ml2[-1]: ml2.pop()   # remove last line, if empty
            ml2.append(mimetype +"="+ desktopfn)
            ml2.append("")
         state="D"
      ml2.append(l)
   ml = os.linesep.join(ml2)
   with open(mlist, "w") as f:
      f.write(ml)
   return 0

def main():
   """
   read cmd line params and start
   :return: 0=ok
   """
   if 0:    # test
      globs.fileextension=".test3"
      globs.filetype="mytype3"
      globs.apppath="~/prg/t/exe3.sh"
      globs.comment="my test-type-3"
      globs.force=1
   
   print("create a mime-type from file-extension for xfce-desktop"+os.linesep)
   
   for arg in sys.argv[1:]:
      p = arg.split("=", 1);
      p1 = ""
      if len(p) > 1: p1 = p[1]
      p=p[0]
      if p in ("-h", "?", "--help", "-?"):
        print("createXfceMimeType " + __version__ + "." + __revision__)
        print(__doc__)
        sys.exit(0)
      if p == "-e": globs.fileextension = p1
      if p == "-p": globs.vendor = p1
      if p == "-t": globs.filetype = p1
      if p == "-f": globs.force = int(p1)
      if p == "-a": globs.apppath = p1
      if p == "-c": globs.comment = p1
      if p == "-i": globs.interactive = 1
      if p == "-v": globs.verbosity = int(p1)
      if p == "-V": print("Version: " + __version__ + "." + __revision__)

   if globs.interactive:
      interactiveParams()
      
   if not globs.fileextension:
      print("createXfceMimeType " + __version__ + "." + __revision__)
      print(__doc__)
      sys.exit(1)
   while globs.fileextension[0] == ".":
      globs.fileextension=globs.fileextension[1:]
   if not globs.filetype:
      globs.filetype = globs.fileextension +"-file"
   globs.filetype = globs.filetype.replace(" ","-")

   ret = 0
   if globs.apppath:
      ret = modMimelist(globs.apppath, f"application/x-{globs.vendor}-{globs.filetype}",
                        globs.comment,  globs.force)

   if ret:   return ret
   return registerMimeType(globs.fileextension, globs.vendor, globs.filetype,
                     globs.comment, globs.apppath, globs.force)

def interactiveParams():
   print("change parameters, or just press [Enter] to unchange.")
   def getit(value):
      va = getattr(globs,value)
      v=input(f"{value} ({va}) ")
      if v: setattr(globs,value,v)
   for v in ("fileextension", "vendor", "filetype", "comment", "apppath"):
      getit(v)
   return 0

if __name__ == "__main__":
   sys.exit(main())
   
#eof
   
