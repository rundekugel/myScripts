#!/usr/bin/env python3
"""
HOTP test script to test 
"""

import pyotp
import time

__author__ = rundekugel@github
__version__ = "1.0.0"

base32encoded_secret = "ABCD"

t2=pyotp.parse_uri('otpauth://totp/issuername:username?secret='+ base32encoded_secret +'&issuer=issuername')
print("tolerance -10 sec: ", t2.generate_otp(round((time.time()-10)/30-.5)) )
print("tolerance -10 sec: ", t2.generate_otp(int((time.time()-10)/30)) )
print("tolerance +10 sec: ", t2.generate_otp(round((time.time()+10)/30-.5)) )

while 1:
	print(round(time.time()) , t2.now(), t2.generate_otp(int((time.time()+0)/30)) )
	print("tolerance -10 sec: ", t2.generate_otp(int((time.time()-10)/30)) )
	print("tolerance +10 sec: ", t2.generate_otp(int((time.time()+10)/30)) )
	print("Time left:", 30-int(time.time()+.5)%30)
	time.sleep(1)

#eof
