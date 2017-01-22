#!/usr/bin/env python3
# pylint: disable=invalid-name, missing-docstring, too-many-locals, too-few-public-methods

from __future__ import print_function

import os
import unittest
import yaml


def partition(ary):
    pivot_index = choose_pivot_index(ary)
    i = 1

    for j in range(1, len(ary) - 1):

        if ary[i] < ary[pivot_index]:
            ary[i], ary[pivot_index] = ary[pivot_index], ary[i]
            cursor += 1

#        elif ary[i] > ary[p]:

    ary[pivot_index], ary[cursor+1] = ary[cursor+1], ary[pivot_index]

    return ary

def choose_pivot_index(ary):
    len(ary)
    return 0

def quicksort(ary):
    # base case
    if len(ary) == 1:
        return ary


class DoTest(unittest.TestCase):
    def test_base(self):
        x = [6, 5, 4, 3, 2, 1]
        y = quicksort(x)
        self.assertEqual(y, sorted(x))

    def test_partition(self):
        x = [3, 8, 2, 4, 1, 99, 100]
        y = partition(x)
        self.assertEqual(y, [2, 1, 3, 4, 8, 99, 100])


    def test_bigfile(self):
        try:
            with open('test_201_countinv.txt') as f:
                x = [int(x.strip()) for x in f]
                y = quicksort(x)
        except OSError:
            pass

        self.assertEqual(y, sorted(x))


def create_dynamic_method(pair):
    def dynamic_test_method(self):
        self.assertEqual(quicksort(pair['t']), sorted(pair['r']))

    return dynamic_test_method

def populate_class(ext=None):
    fn = os.path.basename(__file__)
    tests = []
    tname = fn.rsplit('.')[0:-1]
    if ext:
        tname[0] += "_" + ext

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

populate_class()
populate_class('partition')
