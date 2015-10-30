#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
from hyak import MPI

@MPI
def stringify(x, pool = pool):
  for foo in pool.map(str, x):
    print(foo)

stringify(range(25))