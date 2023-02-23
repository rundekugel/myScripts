#!/usr/bin/env python
"""
python script to delete multiple builds from a TeamCity-server via http-rest-api
(C)opyright by rundekugel 2023
No warranty for lost data or anything else!

usage:
teamCityBuildDelete.py <projectId> [options]

options:
-p=<password>
-u=<user>
-v=<verbosity>
-s=<server name>
-n=<minimum buildnumnber>
-x=<maximum buildnumnber>
"""

import sys
import requests
import xmljson
from xml.etree.ElementTree import fromstring
from xmljson import gdata

def main():
   print("Delete some builds from teamcity...")

   # presets. Fill in your own settings here:
   server = None  #  fqdn, example: "myTeamcity-server.org"
   user = None    #  you may fill in your teamcity user here to prevent typing it always
   pw = None
   locator = None  # the teamcity project identifier i.e. "MyProject_subproject"

   buildmin = 70  # the minimum buildnumber to be deleted
   buildmax = 12001  # the maximum buildnumber to be deleted

   verbosity = 1
   firstfound = None


   for p in sys.argv:
      if p[0] != "-":
         locator = p
      if p[:2] == "-p":
         pw = p[3:]
      if p[:2] == "-u":
         user = p[3:]
      if p[:2] == "-s":
         server = p[3:]
      if p[:2] == "-h":
         print(__doc__)
         return
      if p[:2] == "-v":
         verbosity = int(p[3:])
      if p[:2] == "-n":
         buildmin = int(p[3:])
      if p[:2] == "-x":
         buildmax = int(p[3:])


   if not user:
      user = input("Teamcity-User: ")
   if not pw:
      pw = input("Teamcity-Password: ")
   if not locator:
      locator = input("Locator: ")
   if not server:
      server = input("Server name: ")

   prefix = f"https://{user}:{pw}@{server}"
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
