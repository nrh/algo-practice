#!/usr/bin/env python3
# pylint: disable=invalid-name, missing-docstring, superfluous-parens

import sys

def main(argv):
    print(argv)
    print(kmult(argv[1], argv[2]))

def kmult(upper, lower):
    upper = str(upper)
    lower = str(lower)
    if len(upper) == 1 or len(lower) == 1:
        return str(int(upper) * int(lower))

    # split upper/lower into abcd
    mid = max(int(len(upper)), int(len(lower)))
    mid = int(mid / 2)

    a = upper[0:len(upper)-mid]
    b = upper[len(upper)-mid:]
    c = lower[0:len(lower)-mid]
    d = lower[len(lower)-mid:]

    ac = kmult(a, c)
    bd = kmult(b, d)
    ab = int(a) + int(b)
    cd = int(c) + int(d)
    ab_cd = kmult(ab, cd)
    z = int(ab_cd) - int(bd) - int(ac)

    ac_p = int(ac) * 10**(2*mid)
    z_p = int(z) * 10**mid

    print(ac_p, z_p, bd)
    return str(ac_p + z_p + int(bd))





if __name__ == '__main__':
    sys.exit(main(sys.argv))
