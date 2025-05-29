#!/usr/bin/env python3
"""
HOTP test script to test 
parameter:
    -k=<base32encoded secret>
    -i=<interval>       default=30
    -v=<token>          verify this token
    -t=<tolerance>      tolerance in seconds, default=10
    -V=<verbosity>      0..9
    -L=<loop>           1..oo show actual HOTP-Token in a one-second-loop. 

return value:
    0   token verify success
    1   token verify failed
    2   no token  
    3   key is no base32 secret
    4   no key 
"""

import pyotp
import time
import sys

__author__ = "rundekugel@github"
__version__ = "1.0.1"

class globs:
    base32encoded_secret = None
    intervall=30
    tolerance=10
    verbosity=1
    loop=1

def main():
    token = None
    retval = -1
    
    for p in sys.argv:
        p0,p1= (p.split("=",1) +[None] )[:2]
        print(p0,p1)

        if p0== "-k":
            globs.base32encoded_secret = p1.strip()
            if globs.verbosity:
                print("key from commandline used")
        if p0=="-i":
            globs.intervall=int(p1)
        if p0=="-L":
            globs.loop=int(p1)
        if p0=="-V":
            globs.verbosity=int(p1)
        if p0=="-t":
            globs.tolerance=int(p1)
        if p0=="-v":
            token=p1
        if p0 in ("-h","--help","-?"):
            print(__doc__)
            return 4
            
    if globs.base32encoded_secret is None:
        print("Error! No key given! Try -h for help.")
        return 3

    t2=pyotp.parse_uri('otpauth://totp/issuername:username?secret='+ globs.base32encoded_secret +'&issuer=issuername')
    if globs.verbosity >1:
        print("tolerance -10 sec: ", t2.generate_otp(round((time.time()-10)/globs.intervall-.5)) )
        print("tolerance -10 sec: ", t2.generate_otp(int((time.time()-10)/globs.intervall)) )
        print("tolerance +10 sec: ", t2.generate_otp(round((time.time()+10)/globs.intervall-.5)) )

    if token is not None:
        retval= 1
        if token == t2.now():
            retval= 0
        if token == t2.generate_otp(int((time.time()-globs.tolerance)/globs.intervall)) :
            retval= 0
        if token == t2.generate_otp(int((time.time()+globs.tolerance)/globs.intervall)) :
            retval= 0
        if globs.verbosity:
            if retval:
                print("verify failed!")
            else:
                print("verify successful.")
        return retval
        
    if globs.verbosity == 0:
        return retval
    while globs.loop:
        globs.loop -= 1
        print("Time: ",round(time.time()))
        print("Token: ", t2.now())
        print("Last token -10 sec: ", t2.generate_otp(int((time.time()-10)/globs.intervall)) )
        print("Next token +10 sec: ", t2.generate_otp(int((time.time()+10)/globs.intervall)) )
        print("Time left:", globs.intervall-int(time.time()+.5)%globs.intervall)
        time.sleep(1)
    return retval
    
if __name__ == "__main__":
    sys.exit(main())

#eof
