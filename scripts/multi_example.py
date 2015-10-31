#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
multi_example.py
----------------

This example returns the value of the quadratic equation

  y = ax^2 + bx + c

for a range of values of ``x`` using ``multiprocessing`` 
parallelization. Simply run

>>> python multi_example.py

'''

from __future__ import division, print_function, absolute_import, unicode_literals
from para import multi
import numpy as np

def quadratic(x, a, b, c):
  '''
  The function we're parallelizing
  
  '''
  return a * x ** 2 + b * x + c

print(multi(quadratic, np.arange(10), args = (1, 1, 1), kwargs = {}))