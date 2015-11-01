para
----

Easy parallelization for ``Python`` jobs.

installation
============

Clone the repository and run ``./setup``. This will check if you have ``mpi4py`` installed -- this package is required for ``MPI`` parallelization on a cluster. It will also attempt to update your ``PATH`` and ``PYTHONPATH`` variables in ``~/.profile``, ``~/.bash_profile``, or ``~/.bash_rc``.

examples
========

``para`` is really straightforward. On your computer, ``cd`` into the ``scripts/`` directory and type::

    python multi_example.py

to run a very simple job in parallel using ``Python``'s ``multiprocessing`` module. If you wish to use ``para`` on a computer cluster with ``MPI``, ``cd`` into the ``scripts/`` directory and type::

    para mpi_example.py

to run the same job using ``MPI`` parallelization with ``mpiexec``. This will generate a ``PBS`` script (type ``para -h`` to see available PBS options) and submit it to the queue using ``qsub``. Once the job is complete, the output is stored in ``mpi_example.py.log`` in the same directory.

using ``para`` in your project
==============================

If you want to parallelize a certain part of your code with ``MPI``, you should have a script that looks something like this:

.. code-block:: python

    from para import mpi
    
    def func(x, *args, **kwargs):
        '''
        The function you wish to parallelize
  
        '''
        
        # Do some lengthy calculation
        
        return y
    
    # Call ``func()`` in parallel, once for each element in ``xlist``
    # and store the results in the list ``res``. The options ``args``
    # and ``kwargs`` are any arguments/keywords to be passed to ``func``
    
    res = mpi(func, xlist, args = (), kwargs = {}))

On a computer cluster, simply call::

    para script.py

to submit your job to the queue. You can specify the number of nodes, the walltime, and several other PBS arguments. Just run ``para -h`` to see the complete list.
