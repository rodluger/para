#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
from .mpi_pool import MPIPool
from multiprocessing.pool import Pool
import sys

__all__ = ['MPI', 'MULTI']

def MPI(**pool_kwargs):
  '''
  A function decorator that enables MPI parallelization. This
  decorator endows the function with a ``pool`` instance (passed
  as a kwarg), which can be used to parallelize things internally.
  
  '''
  
  def decorator(func):
    '''
    Note that this is the actual decorator -- a hack to allow
    ``MPI`` to take on arguments as a decorator. See, for instance,
    http://scottlobdell.me/2015/04/decorators-arguments-python/
    
    '''
    
    def wrapper(*args, **kwargs):
      '''
      Two levels down, the actual MPI functionality!
      
      '''
      
      # Set up the MPI pool
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
      
      # Let's pass ``pool`` to the user's function and then call it
      kwargs.update({'pool': pool})
      func(*args, **kwargs)
      
      # When we're done, close the MPI pool
      pool.close()
  
    return wrapper

  return decorator  

def MULTI(**pool_kwargs):
  '''
  A function decorator that enables parallelization via the 
  ``multiprocessing`` module. This decorator endows the function with 
  a ``pool`` instance (passed as a kwarg), which can be used to 
  parallelize things internally.
  
  '''
  
  def decorator(func):
    '''
    Note that this is the actual decorator -- a hack to allow
    ``MULTI`` to take on arguments as a decorator. See, for instance,
    http://scottlobdell.me/2015/04/decorators-arguments-python/
    
    '''
    
    def wrapper(*args, **kwargs):
      '''
      Two levels down, the actual parallelization functionality!
      
      '''
      
      # Initialize the pool
      pool = Pool(**pool_kwargs)
      
      # Let's pass ``pool`` to the user's function and then call it
      kwargs.update({'pool': pool})
      func(*args, **kwargs)

    return wrapper

  return decorator     