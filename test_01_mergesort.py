#!/usr/bin/env python3
# pylint: disable=invalid-name, missing-docstring

from __future__ import print_function

import os
import unittest
import yaml

def mergesort(ary):
    res = []
    # base cases
    l = len(ary)
    if l <= 1:
        return ary

    # split
    mid = int(l/2)
    left = ary[0:mid]
    right = ary[mid:]
    left = mergesort(left)
    right = mergesort(right)

    # merge
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if int(left[i]) > int(right[j]):
            res.append(right[j])
            j += 1
        else:
            res.append(left[i])
            i += 1

    res += left[i:]
    res += right[j:]

    return res

class MergeSortTest(unittest.TestCase):
    def test(self):
        self.assertEqual(mergesort([6, 5, 4, 3, 2, 1]), [1, 2, 3, 4, 5, 6])


def create_dynamic_method(pair):
    def dynamic_test_method(self):
        self.assertEqual(mergesort(pair['t']), pair['r'])

    return dynamic_test_method


fn = os.path.basename(__file__)
tests = []
tname = fn.rsplit('.')[0:-1]
tname.append('yaml')
tname = '.'.join(tname)
try:
    with open(tname, 'r') as y:
        tests = yaml.load(y)
except FileNotFoundError:
    pass

for seq, t in enumerate(tests):
    dynamic_method = create_dynamic_method(t)
    dynamic_method.__name__ = 'test_yaml_{0}'.format(seq)
    setattr(MergeSortTest, dynamic_method.__name__, dynamic_method)
    del dynamic_method
