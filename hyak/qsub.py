#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
qsub.py
-------

Launch a Hyak qsub job.

'''

from __future__ import division, print_function, absolute_import, unicode_literals
import time
import subprocess

PBS_MPI = \
"""
#!/bin/sh
#PBS -l nodes=%(NODES)d:ppn=%(PPN)d,feature=%(PPN)dcore,mem=%(MEM)dgb,walltime=%(WALLTIME)s
%(STDOUT)s
%(STDERR)s
%(EMAIL)s

mpiexec -np $PBS_NP python %(SCRIPT)%(ARGS)
"""

def QSub(script, nodes = 2, ppn = 12, mem = 40, hours = 1., stdout = None, 
         stderr = None, email = None, args = None):
  '''
  
  '''
  
  walltime = time.strftime('%H:%M:%S', time.gmtime(hours * 3600.))
  if stdout is not None:
    stdout = "#PBS -o %s" % stdout
  else:
    stdout = ''
  if stderr is not None:
    stderr = "#PBS -e %s" % stderr
  else:
    stderr = ''
  if email is not None:
    email = "#PBS -M %s\n#PBS -m abe" % email
  else:
    email = ''
  if args is not None:
    args = ' ' + ' '.join(args)
  else:
    args = ''
  
  with open('script.pbs', 'w') as f:
    contents = PBS_MPI % {'NODES': nodes, 'PPN': ppn, 'MEM': mem, 'WALLTIME': walltime,
                          'STDOUT': stdout, 'STDERR': stderr, 'EMAIL': email, 
                          'SCRIPT': script, 'ARGS': args}
    print(contents, file = f)
    
  subprocess.call(['qsub', 'script.pbs'])