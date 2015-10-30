#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
from .mpi_pool import MPIPool
from multiprocessing.pool import Pool
import sys

__all__ = ['MPI', 'MULTI']

def MPI(debug = False, loadbalance = False):
  '''
  
  '''
  
  def decorator(func):
    '''
    
    '''
    
    def wrapper(*args, **kwargs):
      '''
  
      '''
  
      pool = MPIPool(debug = debug, loadbalance = loadbalance)
      if not pool.is_master():
        pool.wait()
        sys.exit(0)
      kwargs.update({'pool': pool})
      func(*args, **kwargs)
      pool.close()
  
    return wrapper

  return decorator  

def MULTI(func):
  '''
  
  '''
  
  def wrapper(*args, **kwargs):
    '''
    
    '''
    
    pool = Pool()
    