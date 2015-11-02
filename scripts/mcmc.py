#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
mcmc.py
-------

An example of how to use ``para`` with the ``emcee`` package. Prints
the time it takes to run a chain in serial versus in parallel with ``para``.

    Serial MCMC: 4.56 seconds
    Parallel MCMC: 1.58 seconds

'''

from __future__ import division, print_function, absolute_import, unicode_literals
import emcee
import numpy as np
import para
import time

def lnlike(x):
  '''
  A very simply log-likelihood function.
  
  '''
  
  # Our prior
  if np.any(np.abs(x) > 10):
    return -np.inf
  
  # Waste some time (i.e., simulate an expensive serial calculation)
  for i in range(1000):
    y = x ** 2
  
  # The log-likelihood
  return np.sum(x ** 2)

def serial():
  '''
  Run MCMC in serial.
  
  '''
  
  p0 = np.random.randn(100,2)
  sampler = emcee.EnsembleSampler(100, 2, lnlike, pool = None)
  p0, _, _ = sampler.run_mcmc(p0, 100)

def parallel():
  '''
  Run MCMC in parallel using ``para``.
  
  '''
  
  pool = para.Pool()
  p0 = np.random.randn(100,2)
  sampler = emcee.EnsembleSampler(100, 2, lnlike, pool = pool)
  p0, _, _ = sampler.run_mcmc(p0, 100)
  pool.close()

# Let's do some timing tests!

t = time.time()
serial()
ts = time.time() - t
print("Serial MCMC: %.2f seconds" % ts)

t = time.time()
parallel()
tp = time.time() - t
print("Parallel MCMC: %.2f seconds" % tp)