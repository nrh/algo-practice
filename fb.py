#!/usr/bin/env python3
from __future__ import print_function

for i in range(1,100):
    s=""
    if i % 3 == 0:
        s+='Fizz'
    if i % 5 == 0:
        s+='Buzz'
    print(s or i)




