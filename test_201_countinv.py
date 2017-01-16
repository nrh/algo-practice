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
    if l <= 1:
        return (0, ary)

    # split
    mid = int(l/2)
    left = ary[0:mid]
    right = ary[mid:]
    (lcount, left) = mergesortcount(left)
    (rcount, right) = mergesortcount(right)
    (scount, merged) = countsplit(left, right)
    count = scount + lcount + rcount

    return count, merged


def countsplit(left, right):
    # merge - count split inversions
    res = []
    i = 0
    j = 0
    scount = 0
    while i < len(left) and j < len(right):
        if int(left[i]) > int(right[j]):
            res.append(right[j])
            j += 1
            scount = scount + len(left) - i
        else:
            res.append(left[i])
            i += 1

    res += left[i:]
    res += right[j:]

    return scount, res


class DoTest(unittest.TestCase):
    def test_base(self):
        self.assertEqual(countinversions([1, 3, 5, 2, 4, 6]), 3)


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
