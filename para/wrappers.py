#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
from .mpi_pool import MPIPool
from multiprocessing.pool import Pool as MultiPool
import inspect
import sys

__all__ = ['multi', 'mpi', 'map', 'Pool']

def KwargsCheck(f, kwargs):
  '''
  
  '''
  
  kw = dict(kwargs)
  try:
    argspec = inspect.getargspec(f)
  except TypeError:
    argspect = inspect.getargspec(f.__init__)
  if not argspec.keywords:
      for key in kw.keys():
          if key not in argspec.args:
              del kw[key]
  return kw

class wrap(object):
  '''
  
  '''
  def __init__(self, f, *args, **kwargs):
    self.f = f
    self.args = args
    self.kwargs = kwargs
  
  def __call__(self, x):
    return self.f(x, *self.args, **self.kwargs)
    
def multi(f, x, args = (), kwargs = {}, method = 'map', **pool_kwargs):
  '''
  
  '''
  
  pool = MultiPool(**KwargsCheck(MultiPool, pool_kwargs)) 
  w = wrap(f, args, kwargs)  
  return getattr(pool, method)(w, x)

def mpi(f, x, args = (), kwargs = {}, method = 'map', **pool_kwargs):
  '''
  
  '''
  
  # Try to create the pool
  try:
    pool = MPIPool(**KwargsCheck(MPIPool, pool_kwargs))
  except ImportError:
    raise ImportError("MPI requires the mpi4py package. Please install it first.")
  except ValueError:
    raise ValueError("Looks like there's only one MPI process available. Did you use the \x1b[01mpara\x1b[39;49;00m command to run your script?")
  
  # If this is a child process, wait for instructions from master
  if not pool.is_master():
    pool.wait()
    sys.exit(0)
      
  w = wrap(f, args, kwargs)  
  res = getattr(pool, method)(w, x)
  pool.close()
  
  return res

def map(f, x, args = (), kwargs = {}, **pool_kwargs):
  '''
  
  '''
  
  try:
    return mpi(f, x, args = args, kwargs = kwargs, method = 'map', **pool_kwargs)
  except (ImportError, ValueError):
    return multi(f, x, args = args, kwargs = kwargs, method = 'map', **pool_kwargs)

class Pool(object):
  '''
  
  '''
  def __init__(self, **pool_kwargs):
  
    try:
      kw = KwargsCheck(MPIPool, pool_kwargs)
      self._pool = MPIPool(**kw)
      self.MPI = True
    except (ImportError, ValueError):
      kw = KwargsCheck(MultiPool, pool_kwargs)
      self._pool = MultiPool(**kw)
      self.MPI = False
    
    if self.MPI:
      if not self._pool.is_master():
        self._pool.wait()
        sys.exit(0)
  
  def map(self, f, x, args = (), kwargs = {}): 
    '''
    
    '''
    if len(args) or len(kwargs):
      w = wrap(f, *args, **kwargs)  
      return self._pool.map(w, x)
    else:
      return self._pool.map(f, x)
  
  def close(self):
    self._pool.close()
    