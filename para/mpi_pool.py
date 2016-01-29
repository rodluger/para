#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
mpi_pool.py
-----------

Adapted from https://groups.google.com/d/msg/mpi4py/OJG5eZ2f-Pg/DrAvbulFxPYJ

'''


from __future__ import division, print_function, absolute_import, unicode_literals
try:
    from mpi4py import MPI
    MPI = MPI
except ImportError:
    MPI = None

class function_wrapper(object):
    def __init__(self, function, arg):
        self.function = function
        self.arg = arg

def error_function(*args):
  raise Exception("Pool was sent tasks before being told what "
                  "function to apply.")

class MPIPool(object):

    def __init__(self, comm = MPI.COMM_WORLD):
        if MPI is None:
            raise ImportError("Please install mpi4py")
        if comm.size <= 1:
            raise ValueError("Tried to create an MPI pool, but there "
                             "was only one MPI process available. "
                             "Need at least two.")
        self.comm = comm
        self.master = 0
        self.workers = set(range(comm.size))
        self.workers.discard(self.master)
        self.function = error_function
        self.size = self.comm.Get_size() - 1
        
    def is_master(self):
        return self.master == self.comm.rank

    def is_worker(self):
        return self.comm.rank in self.workers

    def map(self, function, iterable):
        assert self.is_master()

        comm = self.comm
        workerset = self.workers.copy()
        if function is not self.function:
            self.function = function
            tasklist = [(tid, function_wrapper(function, arg)) for tid, arg in enumerate(iterable)]
        else:
            tasklist = [(tid, arg) for tid, arg in enumerate(iterable)]
        resultlist = [None] * len(tasklist)
        pending = len(tasklist)
        
        while pending:

            if workerset and tasklist:
                worker = workerset.pop()
                taskid, task = tasklist.pop()
                comm.send(task, dest=worker, tag=taskid)

            if tasklist:
                flag = comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
                if not flag: continue
            else:
                comm.Probe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)

            status = MPI.Status()
            result = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            worker = status.source
            workerset.add(worker)
            taskid = status.tag
            resultlist[taskid] = result
            pending -= 1

        return resultlist

    def wait(self):
        if not self.is_worker(): 
            return
        comm = self.comm
        master = self.master
        status = MPI.Status()
        while True:
            task = comm.recv(source=master, tag=MPI.ANY_TAG, status=status)
            if task is None: 
                break
            elif isinstance(task, function_wrapper):
                self.function = task.function
                arg = task.arg
            else:
                arg = task
            result = self.function(arg)
            comm.ssend(result, master, status.tag)

    def close(self):
        if not self.is_master(): 
          return
        for worker in self.workers:
            self.comm.send(None, worker, 0)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

if __name__ == '__main__':

    pool = MPIPool()

    def sq(x): return x*x

    pool.wait()

    if pool.is_master():

        tic = MPI.Wtime()
        res = pool.map(sq, range(100))
        toc = MPI.Wtime()
        
        print(res)
        
        for y, x in zip(res, range(100)):
            assert y == sq(x)

    pool.close()