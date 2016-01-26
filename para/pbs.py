#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
pbs.py
------

Generates a ``PBS`` script and launches a ``qsub`` job on a cluster.

'''

from __future__ import division, print_function, absolute_import, unicode_literals
import os
import subprocess
import re

__all__ = ['qsub']

PBS_MPI = \
"""
#!/bin/sh
%(NAME)s
#PBS -l nodes=%(NODES)d:ppn=%(PPN)d,feature=%(PPN)dcore,mem=%(MEM)dgb,walltime=%(WALLTIME)s
%(STDOUT)s
%(STDERR)s
%(EMAIL)s
%(CMDS)s
cd %(PATH)s
mpiexec -np $PBS_NP python %(SCRIPT)s%(ARGS)s
"""

def StrTime(hours):
  '''
  
  '''
  seconds = int(hours * 3600)
  minutes, seconds = divmod(seconds, 60)
  hours, minutes = divmod(minutes, 60)
  days, hours = divmod(hours, 24)
  return '%02d:%02d:%02d:%02d' % (days, hours, minutes, seconds)
  
def qsub(script, path = None, nodes = 2, ppn = 12, mem = 40, 
         hours = 1., stdout = None, stderr = None, email = None, 
         args = None, logfile = None, cmds = None, name = None):
  '''
  
  '''

  if path is None:
    path = os.getcwd()
  if name is not None:
    name = "#PBS -n %s" % name
  else:
    name = ''
  walltime = StrTime(hours)
  if stdout is not None and stdout == stderr:
    stdout = "#PBS -j oe\n#PBS -o %s" % stdout
    stderr = ''
  else:
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
  if logfile is not None:
    args = args + ' &> ' + logfile
  if cmds is None:
    cmds = ''
  
  # Get the next available script file name
  numbers = [int(re.search('script([0-9]{5}).pbs', f).groups()[0]) for f in os.listdir('.') if re.search('script([0-9]{5}).pbs', f)]
  if len(numbers):
    pbsfile = 'script%05d.pbs' % (max(numbers) + 1)
  else:
    pbsfile = 'script00000.pbs'
  
  with open(pbsfile, 'w') as f:
    contents = PBS_MPI % {'NODES': nodes, 'PPN': ppn, 'MEM': mem, 'WALLTIME': walltime,
                          'STDOUT': stdout, 'STDERR': stderr, 'EMAIL': email, 
                          'SCRIPT': script, 'ARGS': args, 'PATH': path,
                          'CMDS': cmds, 'NAME': name}
    print(contents, file = f)
  
  try:
    subprocess.call(['qsub', pbsfile])
  except FileNotFoundError:
    raise Exception("Unable to launch the script using qsub.")