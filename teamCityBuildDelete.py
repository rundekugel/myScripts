#!/usr/bin/env python
"""
python script to delete multiple builds from a TeamCity-server via http-rest-api
(C)opyright by rundekugel 2023
No warranty for lost data or anything else!

usage:
teamCityBuildDelete.py [projectId] [projectId] [options]

options:
-p=<password>
-u=<user>
-v=<verbosity>
-s=<server name>
-i=<project ID/Entity ID>
-n=<minimum buildnumnber>
-x=<maximum buildnumnber>
-j=<json-config-file>   get data from config file

sample json config:
{
"info":"teamCityBuildDelete Config demo file. jobname, min buildnumber, maxbuildnumber",
"server":"the-ip-or-servername.org",
"user":"John",
"verbosity":2,
"jobs":[
    ["ProjectC_FlasherPayload",36,12000],
    ["Project4_Bootloaderupdate",37,12007],
    ["ProjectC_Bootloader"]
]
}
"""

import sys
import requests
import xmljson
from xml.etree.ElementTree import fromstring
# from xmljson import gdata
import json

class globs:
    verbosity = 2
    pwd = None
    user = "teamcity-user-name"
    server = "server-ip-or-dns.org"


def deleteBuilds(locator, buildmin, buildmax):
    print("Delete some builds from teamcity...")
    print("Job: ", locator)
    print(f"Build {buildmin}..{buildmax}")
    print("User: ", globs.user)

    try:
        if not globs.pwd:
            pw = input("Teamcity-Password: ")
            if pw: globs.pwd = pw

        firstfound = None

        prefix = f"https://{globs.user}:{globs.pwd}@{globs.server}"
        next = f"/app/rest/builds/?locator=buildType:{locator}"
        while next:
            url = prefix + next
            r = requests.get(url)
            ct = r.content.decode()
            if 200 != r.status_code:
                print(f"Status code: {r.status_code}")
                print(ct)
                return 1
            js = xmljson.gdata.data(fromstring(ct))
            bs = js.get("builds")
            if not bs:
                print("no builds!")
                return 2
            next = bs.get("nextHref")
            more = ""
            if next:
                more = "...and more."
            if globs.verbosity:
                print("items found: " + str(bs.get("count")), more)
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
                if globs.verbosity > 1:
                    print(bi)
                n = bi["number"]
                if n >= buildmin and n <= buildmax:
                    weburl = bi.get("webUrl")
                    if not weburl:
                        print("error: no url given!" + bi)
                        continue
                    delurl = prefix + "/app/rest/builds/?locator=" + str(bi["id"])
                    if globs.verbosity:
                        print(f"delete: id {bi['id']} ; build# {n}")
                    requests.delete(delurl)
            next = bs.get("nextHref")
    except:
        print("error!")
    print("Done.")

def main():
   print("Delete some builds from teamcity...")

   # presets. Fill in your own settings here:
   server = None  #  fqdn, example: "myTeamcity-server.org"
   user = None    #  you may fill in your teamcity user here to prevent typing it always
   pw = None
   locator = None  # the teamcity project identifier i.e. "MyProject_subproject"
   projectIds = [
    "myProject1_subprojectB",
    "myP2_subC"
   ]
   buildmin = 36  # the minimum buildnumber to be deleted
   buildmax = 12001  # the maximum buildnumber to be deleted

   jsonfile = None

   for p in sys.argv[1:]:
      if p[0] != "-":
         projectIds.append(p)
      if p[:2] == "-i":
         projectIds.append(p[3:])
      if p[:2] == "-p":
         globs.pwd = p[3:]
      if p[:2] == "-u":
         globs.user = p[3:]
      if p[:2] == "-s":
         globs.server = p[3:]
      if p[:2] == "-h":
         print(__doc__)
         return
      if p[:2] == "-v":
         globs.verbosity = int(p[3:])
      if p[:2] == "-n":
         buildmin = int(p[3:])
      if p[:2] == "-x":
         buildmax = int(p[3:])
      if p[:2] == "-j":
          jsonfile = p[3:]


   if jsonfile:
       with open(jsonfile,"r") as f:
        cfg = json.load(f)
        for key in ["info","server","verbosity","user","pwd"]:
            r = cfg.get(key)
            if r:
                print(f"{key}: {r}")
                if key == "server": globs.server = r
                if key == "verbosity": globs.verbosity = r
                if key == "user": globs.user = r
        globs.pwd = cfg.get("pwd",globs.pwd)
        jobs = cfg.get("jobs")

   if not globs.user:
      globs.user = input("Teamcity-User: ")
   if not globs.pwd:
      globs.pwd = input("Teamcity-Password: ")
   if not projectIds:
      projectIds.append(input("Locator: "))
   if not globs.server:
      globs.server = input("Server name: ")

   for locator in projectIds:
       deleteBuilds(locator, buildmin, buildmax)
   for job in jobs:
       if len(job)>1:   buildmin = job[1]
       if len(job)>2:   buildmax = job[2]
       deleteBuilds(job[0], buildmin, buildmax)

if __name__ == "__main__":
    main()

#eof
