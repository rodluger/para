#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
from hyak import MPI, MULTI
import numpy as np

@MPI()
def sqrt(x, pool = None):
  for foo in pool.map(np.sqrt, x):
    print(foo)

sqrt(range(10))