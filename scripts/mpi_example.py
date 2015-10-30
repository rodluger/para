#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
mpi_example.py
--------------

This example is meant to be called from a PBS script. It calculates
and prints the square roots of all integers from 0 to 99.

>>> launch mpi_example.py -l mpi_example.log

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