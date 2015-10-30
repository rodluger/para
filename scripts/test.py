#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
from hyak import MPI

@MPI
def squareme(x, pool = None):
  for foo in pool.map(lambda x: x ** 2, x):
    print(foo)

squareme(range(10))