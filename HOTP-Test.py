#!/usr/bin/env python3
"""
HOTP test script to test 
"""

import pyotp
import time
import sys

__author__ = "rundekugel@github"
__version__ = "1.0.0"

base32encoded_secret = "ABCD"
intervall=30

for p in sys.argv:
    p0,p1= (p.split("=",1) +[None] )[:2]
    print(p0,p1)

    if p0== "-k":
        base32encoded_secret = p1.strip()
        print("key from commandline used")
    if p0=="-i":
        intervall=int(p1)
        
    

t2=pyotp.parse_uri('otpauth://totp/issuername:username?secret='+ base32encoded_secret +'&issuer=issuername')
print("tolerance -10 sec: ", t2.generate_otp(round((time.time()-10)/intervall-.5)) )
print("tolerance -10 sec: ", t2.generate_otp(int((time.time()-10)/intervall)) )
print("tolerance +10 sec: ", t2.generate_otp(round((time.time()+10)/intervall-.5)) )

while 1:
	print(round(time.time()) , t2.now(), t2.generate_otp(int((time.time()+0)/intervall)) )
	print("tolerance -10 sec: ", t2.generate_otp(int((time.time()-10)/intervall)) )
	print("tolerance +10 sec: ", t2.generate_otp(int((time.time()+10)/intervall)) )
	print("Time left:", intervall-int(time.time()+.5)%intervall)
	time.sleep(1)

#eof
