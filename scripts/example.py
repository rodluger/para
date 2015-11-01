#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
example.py
----------

This example returns the value of the quadratic equation

  y = ax^2 + bx + c

for a range of values of ``x``, calculated in parallel. 

To parallelize with ``multiprocessing``, simply run

>>> python example.py

Or, to parallelize using ``MPI`` (assuming you have
``mpi4py`` installed and are running on a cluster), run

>>> mpi example.py

to send a PBS job to the queue. By default, the output will be 
printed to a log file in the same directory.

'''

from __future__ import division, print_function, absolute_import, unicode_literals
try:
  from para import map
except:
  # If ``para`` isn't installed, we'll just use the built-in ``map`` function
  pass
import numpy as np

def quadratic(x, a, b, c):
  '''
  The function we're parallelizing
  
  '''
  return a * x ** 2 + b * x + c

for res in map(quadratic, np.arange(100), args = (1, 1, 1), kwargs = {}):
  print(res)