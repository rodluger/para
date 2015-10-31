#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
multi_example.py
----------------

This example calculates and prints the square root of all
integers between 0 and 9 using ``multiprocessing`` 
parallelization. Just run

>>> python multi_example.py

'''

from __future__ import division, print_function, absolute_import, unicode_literals
from para import MULTI
import numpy as np

@MULTI()
def sqrt(x, pool = None):
  for foo in pool.map(np.sqrt, x):
    print(foo)

if __name__ == '__main__':
  sqrt(range(10))
