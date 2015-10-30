#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
from hyak.pools import MPI

def f(pool):
  for foo in pool.map(str, range(25)):
    print(foo)

MPI(f)