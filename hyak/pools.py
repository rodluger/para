#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
from .mpi_pool import MPIPool
from multiprocessing.pool import Pool
import sys

def MPI(func):
  '''
  
  '''
  
  pool = MPIPool()
  if not pool.is_master():
    pool.wait()
    sys.exit(0)
  
  func(pool = pool)