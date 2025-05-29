echo multiple nslookup: $*
nslookup $*
nslookup -q=ns $*
nslookup  -q=txt $*
#ns=$(nslookup -q=ns google.de|grep -m1 nameserver)
ns=$(nslookup -q=ns $* |grep -m1 nameserver|sed -r 's/.*=//g')
echo ns=$ns
echo any:
nslookup -q=any $* $ns
echo mx:
nslookup -q=mx $* $ns
nslookup -q=aaaa $* $ns
echo txt:
nslookup -q=txt $* $ns
echo cname:
nslookup -q=cname $* $ns


