#!/usr/bin/env para
# -*- coding: utf-8 -*-
'''
mpi_example.py
--------------

This example returns the value of the quadratic equation

  y = ax^2 + bx + c

for a range of values of ``x`` using ``MPI``
parallelization. Simply run

>>> launch multi_example.py

By default, output is saved in ``mpi_example.py.log``.

'''

from __future__ import division, print_function, absolute_import, unicode_literals
from para import mpi
import numpy as np

def quadratic(x, a, b, c):
  '''
  The function we're parallelizing
  
  '''
  return a * x ** 2 + b * x + c

print(mpi(quadratic, np.arange(10), args = (1, 1, 1), kwargs = {}))
