#!/usr/bin/env python
"""
create a file from part of bigger file with keywords for start and end
"""

import sys,os


class globs:
   start=b"%PDF"
   end=b"%%EOF"
   state = 0
   fnout = "fout"
   bs = 0x1000000
   usestdout = 0
   # offset = 35744888
   #offset = 82624512
   #offset = 116428800
   offset = 0
   # length = 0
   cn=1

def getnewfn():
   fn= globs.fnout+str(globs.cn)+".pdf"
   if os.path.exists(fn):
      globs.cn+=1
      return getnewfn()
   return fn
      
      

def main():   
   fn = "/media/user/hdd"
   if len(sys.argv)>1 and sys.argv[1][0] != "-":
      fn = sys.argv[1]
   for arg in sys.argv:
      if arg[:2]=="-o": globs.offset = int(arg[3:],0)
      
   print("use file: %s with offset %i = 0x%x"%(fn,globs.offset,globs.offset))
   print("search for start:%s/end:%s"%(globs.start,globs.end))
   f=open(fn, "rb")
   if globs.offset:
      f.seek(globs.offset)
   pdf = b""
   posstart = globs.offset
   p1 = 0
   doit = 1
   length = globs.offset
   r=b""

   while (doit):
      r=b""
      try:
         r=f.read(globs.bs)
      except:
         r=b""
      p=0

      # if 1: # globs.state == 0 or globs.state == 2:
      p = r.find(globs.start)
      if p > -1:  #start found
         while 1:
            if globs.state == 1: # again?
               p2 = r.find(globs.end)
               if (p2>-1):
                  if (p2<p):  # end before start available
                     print("stop!")
                     break
                  else:
                     print(os.linesep+"error! found 2nd pdf start")
                     print("-3-")
                     # posstart += p
                     break
               posstart = length + p
               break
            else:
               posstart +=p
               if not globs.usestdout:
                  print("pos:" + str(posstart)+" ="+hex(posstart))
            globs.state = 1
            print(end="1")
            r = r[p:]
            break
      #check for end
      if globs.state == 1:
         p = r.find(globs.end)
         if p > -1:
            globs.state = 2
            print(end="0")
            p+=len(globs.end)+1
            pdf += r[:p]
            doit-=1
         else:
            pdf += r
      if globs.state == 0:
         posstart += len(r)
      length += len(r)

   f.close()
   globs.state = 0
   globs.offset = posstart+len(pdf)
   if not globs.fnout or globs.fnout=="-":
      print(pdf)
      print(r)
   else:
      fn = getnewfn()
      print("L:"+str(len(pdf)))
      print("Writing to:"+str(fn))
      f=open(fn,"wb")
      f.write(pdf)
      f.close()
      globs.cn += 1
      print("")
   return length


while 1:
   r = main()
   sys.argv=[]




         
   

