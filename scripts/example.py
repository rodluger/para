#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
example.py
----------

'''

from __future__ import division, print_function, absolute_import, unicode_literals
from hyak import MPI, MULTI
import numpy as np

@MPI()
def sqrt(x, pool = None):
  for foo in pool.map(np.sqrt, x):
    print(foo)

if __name__ == '__main__':
  sqrt(range(100))