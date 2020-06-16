
#!/bin/usr python
"""
draw color palette in HTML for TFT colors possible with 2 bit per color
"""

import time

hh = ["00","55","aa","ff"]

print("<table>RGB222")
for r in range(4):
  print("<tr>")
  for g in range(4):
    for b in range(4):
      ch = hh[r] +hh[g] +hh[b]
      print('<th style="background-color: '+ ch +'">%i%i%i</th>'%(r,g,b))
    print("\r\n")
  print("</tr>\r\n")
print("</table>")
 
 
print("<table>RGB221")
for r in range(4):
  print("<tr>")
  for g in range(4):
    for b in range(2):
      ch = hh[r] +hh[g] +hh[b*3]
      print('<th style="background-color: '+ ch +'">%i%i%i</th>'%(r,g,b))
  print("</tr>\r\n")
print("</table>")
 
 
while(1):
  time.sleep(.1)
  
#eof
