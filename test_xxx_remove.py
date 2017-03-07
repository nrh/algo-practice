
#!/usr/bin/env python3
# pylint: disable=invalid-name, missing-docstring, too-many-locals, too-few-public-methods

from __future__ import print_function

import os
import unittest
import yaml


def prune_array(A, s):
    ''' remove elements in A with value s'''
    i = 0
    p = len(A) - 1

    while i <= p:
        if A[i] == s:
            A[i], A[p] = A[p], A[i]
            p -= 1
        i += 1

    return A[0:p + 1]


class DoTest(unittest.TestCase):
    def test_base(self):
        r = prune_array([4, 3, 2, 1, 2, 3, 6], 2)
        self.assertEqual(sorted(r), sorted([4, 3, 1, 3, 6]))



def create_dynamic_method(args, seq):
    def dynamic_test_method(self):
        A, s, r = args.get('t'), args.get('s'), args.get('r')

        self.assertEqual(prune_array(A, s), r)


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
    DoTest().test_base()
