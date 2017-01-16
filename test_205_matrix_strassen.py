#!/usr/bin/env python3
# pylint: disable=invalid-name, missing-docstring, too-many-locals

from __future__ import print_function

import os
import unittest
import yaml

class MatrixMismatchError(Exception):
    pass


class MatrixElementError(Exception):
    pass

def carve(m1, m2):
    return m1[0][0], m1[0][1], m1[1][0], m1[1][1], m2[0][0], m2[0][1], m2[1][0], m2[1][1]

def matrixmult(m1, m2):
    # are these correctly sized?
    # [1,2,3] [4,5,6] x [7,8] [9,10] [11,12]
    # shouldn't we be able to pad them with zeros? hmmm
    if len(m1[0]) != len(m2):
        raise MatrixMismatchError

    for m in m1, m2:
        ilen = len(m[0])
        for ary in m:
            if len(ary) != ilen:
                raise MatrixElementError
    a, b, c, d, e, f, g, h = carve(m1, m2)
    # base case
    p1 = a * (f - h)
    p2 = (a + b) * h
    p3 = (c + d) * e
    p4 = d * (g - e)
    p5 = (a + d) * (e + h)
    p6 = (b - d) * (g + h)
    p7 = (a - c) * (e + f)

    return [p5 + p4 - p2 + p6, p1 + p2], [p3 + p4, p1 + p5 - p3 - p7]

class DoTest(unittest.TestCase):
    def test_base(self):
        self.assertEqual(matrixmult([[1, 2], [3, 4]],
                                    [[5, 6], [7, 8]]),
                         ([19, 22], [43, 50]))


def create_dynamic_method(pair):
    def dynamic_test_method(self):
        self.assertEqual(matrixmult(pair['t'][0], pair['t'][1]),
                         (pair['r'][0], pair['r'][1]))

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
