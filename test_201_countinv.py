#!/usr/bin/env python3
# pylint: disable=invalid-name, missing-docstring

from __future__ import print_function

import os
import unittest
import yaml

def countinversions(ary):
    return mergesortcount(ary)[0]

def mergesortcount(ary):
    # base cases
    l = len(ary)
    if l > 1:
        mid = l//2
        left = ary[:mid]
        right = ary[mid:]
        lcount, left = mergesortcount(ary[:mid])
        rcount, right = mergesortcount(ary[mid:])
        scount, merged = splitcount(left, right)
        count = scount + lcount + rcount
        return count, merged
    else:
        return 0, ary

def splitcount(left, right):
    # merge - count split inversions
    res = []
    scount = 0
    while left and right:
        if int(left[0]) <= int(right[0]):
            res.append(left.pop(0))
        else:
            scount += len(left)
            res.append(right.pop(0))

    res += left
    res += right

    return scount, res


class DoTest(unittest.TestCase):
    def test_base(self):
        self.assertEqual(countinversions([1, 3, 5, 2, 4, 6]), 3)

    def test_bigfile(self):
        try:
            with open('test_201_countinv.txt') as f:
                i, s = mergesortcount([int(x.strip()) for x in f])
        except OSError:
            pass

        self.assertEqual(i, 2407905288)


def create_dynamic_method(pair):
    def dynamic_test_method(self):
        self.assertEqual(countinversions(pair['t']), pair['r'])

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
