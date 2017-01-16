#!/usr/bin/env python3
# pylint: disable=invalid-name, missing-docstring

from __future__ import print_function

import os
import unittest
import yaml

def mult(pair):
    lower = str(pair[0])
    upper = str(pair[1])

    p1 = 0
    p2 = ''
    pi = 0
    li = -1
    ui = -1

    lbound = len(lower) * -1
    ubound = len(upper) * -1

    carry = 0

    while li >= lbound:
        while ui >= ubound:
            subp = int(lower[li]) * int(upper[ui])
            subp += carry

            if len(str(subp)) == 2:
                carry = int(str(subp)[-2])
            else:
                carry = 0

            x = str(subp)[-1]

            p2 = x + p2
            print(subp, carry, p2)
            ui -= 1

        if carry:
            p2 = str(carry) + p2
            carry = 0

        pad = ''.join('0' * pi)
        pi += 1
        p2 = p2 + pad
        p1 += int(p2)
        li -= 1
        ui = -1
        p2 = ''

    return p1

class DoTest(unittest.TestCase):
    def test_base(self):
        self.assertEqual(mult([6, 5]), 30)


def create_dynamic_method(pair):
    def dynamic_test_method(self):
        self.assertEqual(mult(pair['t']), pair['r'])

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
