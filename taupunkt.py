#!/usr/bin/env python
"""
Berechne Taupunkt aus Temperatur(C) und Luftfeuchte(rel.)
(C) 2024 rundekugel @ github
"""

import sys
import math

def taupunkt(Tc, rel):
    """Berechne Taupunkt aus Temperatur(C) und Luftfeuchte(rel.)"""
    # Parameter:
    a = 7.5; b = 237.3  # für T >= 0
    # a = 7.6, b = 240.7 für T < 0 über Wasser (Taupunkt)
    # a = 9.5, b = 265.5 für T < 0 über Eis (Frostpunkt)

    tk = Tc + 273.15
    sdd = 6.1078 * 10**((a*Tc)/(b+Tc))
    dd = rel/100 * sdd

    v = math.log10(dd / 6.1078)
    tp = b*v/(a-v)
    return tp

def main(t,r):
    print(round(taupunkt(t,r), 2))
    return 0

if __name__ == "__main__":
    sys.exit(main(float(sys.argv[1]), float(sys.argv[2])))
# eof
