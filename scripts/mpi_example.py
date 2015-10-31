#!/usr/bin/env para
# -*- coding: utf-8 -*-
'''
mpi_example.py
--------------

This example calculates and prints the square root of all
integers between 0 and 9 using MPI parallelization on Hyak.
Just run

>>> launch mpi_example.py

By default, output is saved in ``mpi_example.py.log``.

'''

from __future__ import division, print_function, absolute_import, unicode_literals
from para import MPI
import numpy as np

@MPI()
def sqrt(x, pool = None):
  for foo in pool.map(np.sqrt, x):
    print(foo)

if __name__ == '__main__':
  sqrt(range(10))
