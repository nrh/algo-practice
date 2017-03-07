#!/usr/bin/env python3
# pylint: disable=invalid-name, missing-docstring, too-many-locals, too-few-public-methods

from __future__ import print_function

import os
from random import randint
import unittest
import yaml


def _partition(A, l=0, r=None):
    '''O(n) where n==r-l+1'''
    p = choose_pivot_random(A, l, r)
    c = 0
    if p != l:
        A[l], A[p] = A[p], A[l]
        p = l

    for j in range(l + 1, r + 1):
        c += 1
        if A[j] <= A[l]:
            p += 1
            A[p], A[j] = A[j], A[p]

    A[p], A[l] = A[l], A[p]

    return p, c

def choose_pivot_random(A, l, r):
    _ = A
    return randint(l, r)

def _quicksort(A, l, r):
    if r is None:
        r = len(A) - 1

    count = 0
    if l < r:
        p, count = _partition(A, l, r)
        count += quicksort(A, l, p - 1)
        count += quicksort(A, p + 1, r)
    return count

def quicksort(A, l=None, r=None):
    if l is None:
        l = 0
    if r is None:
        r = len(A) - 1
    return _quicksort(A, l, r)


class DoTest(unittest.TestCase):
    def test_base(self):
        A = [6, 5, 4, 3, 2, 1]
        c = quicksort(A)
        print('comparisons={0}'.format(c))
        self.assertEqual(A, sorted(A))

    def test_partition(self):
        A = [3, 8, 2, 5, 1, 4, 7, 6]
        p, c = _partition(A, 0, len(A) - 1)
        print('comparisons={0}'.format(c))
        for e in A[0:p]:
            self.assertTrue(e < A[p], '{0} < {1} == False!'.format(e, A[p]))

        for e in A[p+1:]:
            self.assertTrue(e > A[p], '{0} > {1} == False!'.format(e, A[p]))
        return

    def test_bigfile(self):
        try:
            with open('test_301_quicksort.txt') as f:
                A = [int(x.strip()) for x in f]
                c = quicksort(A)
        except OSError:
            pass

        print('comparisons={0}'.format(c))
        self.assertEqual(A, sorted(A))
        return


def create_dynamic_method(args, seq, ext=None):
    def dynamic_test_method(self):
        A = args.get('t')
        c = quicksort(A)
        print('comparisons={0}'.format(c))
        self.assertEqual(A, sorted(args['r']))
        counts = args.get('c')
        if counts:
            self.assertEqual(c, counts[2])

    def dynamic_test_method_partition(self):
        A = args.get('t')
        left = args.get('left') or 0
        right = args.get('right') or len(A) - 1

        p, c = _partition(A, left, right)
        print('comparisons={0}'.format(c))
        for e in A[left:p]:
            self.assertTrue(e < A[p], '{0} < {1} == False!'.format(e, A[p]))

        for e in A[p+1:right]:
            self.assertTrue(e > A[p], '{0} > {1} == False!'.format(e, A[p]))

    if ext:
        name = 'test_yaml_{0}_{1}'.format(ext, seq)
    else:
        name = 'test_yaml_{0}'.format(seq)

    if ext == 'partition':
        return name, dynamic_test_method_partition

    return name, dynamic_test_method

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
        name, dynamic_method = create_dynamic_method(t, seq, ext)
        dynamic_method.__name__ = name
        setattr(DoTest, dynamic_method.__name__, dynamic_method)
        del dynamic_method

populate_class()

if __name__ == '__main__':
    print(rselect([10, 8, 3, 4], 3))
