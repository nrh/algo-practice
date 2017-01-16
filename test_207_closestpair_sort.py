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

    def __repr__(self):
        return "r({},{})".format(self.x, self.y)

    def __str__(self):
        return "p({},{})".format(self.x, self.y)

    def is_equal(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def dist(self, p2):
        dx = p2.x - self.x
        dy = p2.y - self.y
        return math.sqrt(dx**2 + dy**2)

    def as_tuple(self):
        return [self.x, self.y]


def closestpair(pointlist):
    plist = [Point(xy[0], xy[1]) for xy in pointlist]
    p_sorted_x = sorted(plist, key=lambda foo: foo.x)
    p_sorted_y = sorted(plist, key=lambda foo: foo.y)
    best = closest_pair(p_sorted_x, p_sorted_y)
    return sorted([best[0].as_tuple(), best[1].as_tuple()])

def closest_pair(p_x, p_y):
    closest = []
    z = max(len(p_x), len(p_y))
    # base case, just brute force it

    if z <= 3:
        print('inside sorting x{}'.format(p_x))
        print('inside sorting y{}'.format(p_y))
        dist = math.inf
        closest = []
        for i, x in enumerate(p_x):
            for j, y in enumerate(p_y):
                if not x.is_equal(y):
                    td = p_x[i].dist(p_y[j])
                    if td < dist:
                        dist = td
                        closest = [p_x[i], p_y[j]]
        print('found {} d={}'.format(closest, dist))
        return closest

    print('outside sorting x{}'.format(p_x))

    mid = int(len(p_x)/2)
    q_x = p_x[0:mid]
    r_x = p_x[mid:]
    q_y = p_y[0:mid]
    r_y = p_y[mid:]

    p1, q1 = closest_pair(q_x, q_y)
    p2, q2 = closest_pair(r_x, r_y)
    min_dist = min(p1.dist(q1), p2.dist(q2))
    best_pair = min([p1, q1], [p2, q2], key=lambda x: x[0].dist(x[1]))
    p3, q3 = closest_split_pair(p_x, p_y, min_dist, best_pair)
    print('p1q1={}{} d={}'.format(p1, q1, p1.dist(q1)))
    print('p2q2={}{} d={}'.format(p2, q2, p2.dist(q2)))
    print('p3q3={}{} d={}'.format(p3, q3, p3.dist(q3)))

    # return best of [p1,p2][q1,q2][p3,q3]
    best = min([p1, q1], [p2, q2], [p3, q3], key=lambda x: x[0].dist(x[1]))
    print('best={}, d={}'.format(best, best[0].dist(best[1])))
    return best

def closest_split_pair(p_x, p_y, delta, best_pair):
    mx = p_x[len(p_x)//2].x
    s_y = [n for n in p_y if mx - delta <= n.x <= mx + delta]
    print('searching sy{} from py{} with delta {}'.format(s_y, p_y, delta))
    best = delta
    for i, p in enumerate(s_y):
        for j in range(1, min(8, (len(s_y)-i))):
            print('i={},j={},s_y={}'.format(i, j, len(s_y)))
            q = s_y[i+j]
            print('p={},q={}'.format(p,q))
            dist = p.dist(q)
            if dist < best:
                best_pair = [p, q]
                best = dist
    print('found best {} d={}'.format(best_pair, best))
    return best_pair


class DoTest(unittest.TestCase):
    def test_base(self):
        x = closestpair([[1, 2], [3, 4], [5, 7]])
        self.assertEqual(x, [[1, 2], [3, 4]])

    def test_points(self):
        p1 = Point(5,3)
        p2 = Point(-1231231,999999999)
        self.assertEqual(p1.dist(p2), p2.dist(p1))


def create_dynamic_method(pair):
    def dynamic_test_method(self):
        self.assertEqual(closestpair(pair['t']), sorted(pair['r']))

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
        if 'name' in t:
            dynamic_method.__name__ += '_{0}'.format(t['name'])

        setattr(DoTest, dynamic_method.__name__, dynamic_method)
        del dynamic_method

populate_class()

if __name__ == '__main__':
    x=DoTest()
    x.test_yaml_1_split()
