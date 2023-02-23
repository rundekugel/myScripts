#!/usr/bin/env python
""" 
python script to delete multiple builds from a TeamCity-server via http-rest-api
(C)opyright by rundekugel 2023
No warranty for lost data or anything else!
"""

import requests
import xmljson
from xml.etree.ElementTree import fromstring
from xmljson import gdata

def main():
   print("Delete some builds from teamcity...")

   user = None # you may fill in your user here to prevent typing it always
   pw = None
   user = input("Teamcity-User: ")
   pw = input("Teamcity-Password: ")
   locator = "TheProjectName"

   buildmin = 70  # the minimum buildnumber to be deleted
   buildmax = 9001  # the maximum buildnumber to be deleted

   verbosity = 1
   firstfound = None

   prefix = f"https://{user}:{pw}@teamcity-example-server.org"
   next = f"/app/rest/builds/?locator=buildType:{locator}"
   while next:
      url = prefix + next
      r = requests.get(url)
      ct = r.content.decode()
      if ct[0] != "<":
         print(ct, "no data! possible wrong password?")
         return 1
      js = xmljson.gdata.data(fromstring(ct))
      bs=js.get("builds")
      if not bs:
         print("no builds!")
         return 2
      next = bs.get("nextHref")
      more = ""
      if next:
         more = "...and more."
      if verbosity:
         print("items found: "+str(bs.get("count")), more)
      b = bs.get("build")
      if not b:
         print("no build!")
         return 3
      while b:
         bi = b.pop()
         if not bi:
            break
         if not firstfound:
            firstfound = bi
         if verbosity >1:
            print(bi)
         n = bi["number"]
         if n > buildmin and n < buildmax:
            weburl = bi.get("webUrl")
            if not weburl:
               print("error: no url given!"+bi)
               continue
            delurl = prefix + "/app/rest/builds/?locator="+str(bi["id"])
            if verbosity:
               print(f"delete: id {bi['id']} ; build# {n}")
            requests.delete(delurl)
      next = bs.get("nextHref")

main()

#eof
