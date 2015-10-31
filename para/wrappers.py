#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
from .mpi_pool import MPIPool
from multiprocessing.pool import Pool
import sys

__all__ = ['multi', 'mpi']

class wrap(object):
  '''
  
  '''
  def __init__(self, f, args, kwargs):
    self.f = f
    self.args = args
    self.kwargs = kwargs
  
  def __call__(self, x):
    return self.f(x, *self.args, **self.kwargs)
    
def multi(f, x, args = (), kwargs = {}, **pool_kwargs):
  '''
  
  '''
  
  pool = Pool(**pool_kwargs)  
  w = wrap(f, args, kwargs)  
  return list(pool.map(w, x))

def mpi(f, x, args = (), kwargs = {}, **pool_kwargs):
  '''
  
  '''
  
  # Try to create the pool
  try:
    pool = MPIPool(**pool_kwargs)
  except ImportError:
    raise ImportError("MPI requires the mpi4py package. Please install it first.")
  except ValueError:
    raise Exception("Looks like there's only one MPI process available. Try using the ``launch`` command.")
  
  # If this is a child process, wait for instructions from master
  if not pool.is_master():
    pool.wait()
    sys.exit(0)
    
  pool = Pool(**pool_kwargs)  
  w = wrap(f, args, kwargs)  
  res = list(pool.map(w, x))
  pool.close()
  
  return res