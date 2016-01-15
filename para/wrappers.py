#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
from .mpi_pool import MPIPool
from multiprocessing.pool import Pool as MultiPool
import inspect
import sys

__all__ = ['multi', 'mpi', 'map', 'Pool']

class Wrap(object):
  '''
  Wrapper around an arbitrary function that stores *args and **kwargs
  and permits the function to be called with a single argument (the first one).
  
  '''
  def __init__(self, f, *args, **kwargs):
    self.f = f
    self.args = args
    self.kwargs = kwargs

  def __call__(self, x):
    return self.f(x, *self.args, **self.kwargs)

def FilterKwargs(f, kwargs):
  '''
  Removes any entries from the dict ``kwargs`` that are not
  permitted keyword arguments to callable ``f``.
  
  '''
  
  kw = dict(kwargs)
  try:
    argspec = inspect.getargspec(f)
  except TypeError:
    argspec = inspect.getargspec(f.__init__)
  if not argspec.keywords:
      for key in kwargs.keys():
          if key not in argspec.args:
              del kw[key]
  return kw
    
def multi(f, x, args = (), kwargs = {}, method = 'map', **pool_kwargs):
  '''
  Applies the ``map`` method in a ``multiprocessing`` pool instance to the
  callable ``f`` with input list ``x``.
  
  '''
  
  pool = MultiPool(**FilterKwargs(MultiPool, pool_kwargs)) 
  w = Wrap(f, *args, **kwargs)  
  return getattr(pool, method)(w, x)

def mpi(f, x, args = (), kwargs = {}, method = 'map', **pool_kwargs):
  '''
  Applies the ``map`` method in an ``MPI`` pool instance to the
  callable ``f`` with input list ``x``.
  
  '''
  
  # Try to create the pool
  try:
    pool = MPIPool(**FilterKwargs(MPIPool, pool_kwargs))
  except ImportError:
    raise ImportError("MPI requires the mpi4py package. Please install it first.")
  except ValueError:
    raise ValueError("Looks like there's only one MPI process available. Did you use the \x1b[01mpara\x1b[39;49;00m command to run your script?")
  
  # If this is a child process, wait for instructions from master
  if not pool.is_master():
    pool.wait()
    sys.exit(0)
      
  w = Wrap(f, *args, **kwargs)  
  res = getattr(pool, method)(w, x)
  pool.close()
  
  return res

def call(f, x, args = (), kwargs = {}, **pool_kwargs):
  '''
  Invokes ``mpi`` or ``multi`` depending on whether or not an MPI environment is available.
  
  '''
  
  try:
    return mpi(f, x, args = args, kwargs = kwargs, method = 'map', **pool_kwargs)
  except (ImportError, ValueError):
    return multi(f, x, args = args, kwargs = kwargs, method = 'map', **pool_kwargs)

class Pool(object):
  '''
  A wrapper around ``Pool`` objects in ``multiprocessing`` and ``mpi4py``. As of now,
  this class has a single method, ``map``, which invokes the corresponding method in
  either the ``multiprocessing`` or ``mpi4py`` pool objects.
  
  '''
  def __init__(self, **pool_kwargs):
  
    try:
      self._pool = MPIPool(**FilterKwargs(MPIPool, pool_kwargs))
      self.MPI = True
    except (ImportError, ValueError):
      self._pool = MultiPool(**FilterKwargs(MultiPool, pool_kwargs))
      self.MPI = False
    
    if self.MPI:
      if not self._pool.is_master():
        self._pool.wait()
        sys.exit(0)
  
  def map(self, f, x, args = (), kwargs = {}): 
    '''
    
    '''
    if len(args) or len(kwargs):
      w = Wrap(f, *args, **kwargs)  
      return self._pool.map(w, x)
    else:
      return self._pool.map(f, x)
  
  def close(self):
    self._pool.close()
    