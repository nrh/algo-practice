#!/usr/bin/env python3
# pylint: disable=invalid-name, missing-docstring, too-many-locals, too-few-public-methods

from __future__ import print_function

import os
import unittest
import yaml


def elements_with_sum(A, s):
    ''' find elements in A with sum s'''
    i = 0

    while i < len(A):
        j = i + 1
        while j < len(A):
            if A[i] + A[j] == s:
                return [A[i], A[j]]
            j += 1
        i += 1

    return


class DoTest(unittest.TestCase):
    def test_base(self):
        r = elements_with_sum([1, 2, 4, 7, 11, 15], 15)
        self.assertEqual(r, [4, 11])



def create_dynamic_method(args, seq):
    def dynamic_test_method(self):
        A, s, r = args.get('t'), args.get('s'), args.get('r')

        self.assertEqual(elements_with_sum(A, s), r)


    name = 'test_yaml_{0}'.format(seq)
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
        name, dynamic_method = create_dynamic_method(t, seq)
        dynamic_method.__name__ = name
        setattr(DoTest, dynamic_method.__name__, dynamic_method)
        del dynamic_method

populate_class()

if __name__ == '__main__':
    print(elements_with_sum([1, 2, 4, 7, 11, 15], 15))
    DoTest().test_base()
