#!/usr/bin/env python3
# pylint: disable=invalid-name, missing-docstring, too-many-locals, too-few-public-methods

from __future__ import print_function

import os
import unittest
import math
import yaml


class Point(object):
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def dist(self, p2):
        dx = p2.x - self.x
        dy = p2.y - self.y
        return math.sqrt(dx**2 + dy**2)

    def as_tuple(self):
        return [self.x, self.y]


def closestpair(pointlist):
    plist = [Point(xy[0], xy[1]) for xy in pointlist]

    # brute force method
    dist = plist[0].dist(plist[1])
    print(dist)
    closest = [plist[0].as_tuple(), plist[1].as_tuple()]
    z = len(plist)
    for i in range(z):
        for j in range(z):
            if j != i: # don't compare same elements, they're very close!`
                td = plist[i].dist(plist[j])
                if td < dist:
                    dist = td
                    closest = [plist[i].as_tuple(), plist[j].as_tuple()]

    return closest

class DoTest(unittest.TestCase):
    def test_base(self):
        self.assertEqual(closestpair([[1, 2], [3, 4], [5, 7]]),
                         [[1, 2], [3, 4]])


def create_dynamic_method(pair):
    def dynamic_test_method(self):
        self.assertEqual(closestpair(pair['t']), pair['r'])

    return dynamic_test_method

def populate_class():
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

populate_class()
