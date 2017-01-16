#!/usr/bin/env python3
# pylint: disable=invalid-name, missing-docstring, superfluous-parens

from __future__ import print_function

import os
import unittest
import yaml

def kmult(pair):
    upper = str(pair[0])
    lower = str(pair[1])
    if len(upper) == 1 or len(lower) == 1:
        return int(upper) * int(lower)

    # split upper/lower into abcd
    mid = max(int(len(upper)), int(len(lower)))
    mid = int(mid / 2)

    a = int(upper[0:len(upper)-mid])
    b = int(upper[len(upper)-mid:])
    c = int(lower[0:len(lower)-mid])
    d = int(lower[len(lower)-mid:])

    ac = kmult([a, c])
    bd = kmult([b, d])
    ab_cd = kmult([a+b, c+d])
    z = ab_cd - bd - ac

    ac_p = ac * 10**(2*mid)
    z_p = z * 10**mid

    return ac_p + z_p + bd


class DoTest(unittest.TestCase):
    def test_base(self):
        self.assertEqual(kmult([5, 6]), 30)


def create_dynamic_method(pair):
    def dynamic_test_method(self):
        self.assertEqual(kmult(pair['t']), pair['r'])

    return dynamic_test_method


fn = os.path.basename(__file__)
tests = []
tname = fn.rsplit('.')[0:-1]
tname.append('yaml')
tname = '.'.join(tname)
try:
    with open(tname, 'r') as y:
        tests = yaml.load(y)
except OSError:
    pass

for seq, t in enumerate(tests):
    dynamic_method = create_dynamic_method(t)
    dynamic_method.__name__ = 'test_yaml_{0}'.format(seq)
    setattr(DoTest, dynamic_method.__name__, dynamic_method)
    del dynamic_method
