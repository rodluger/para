para
----

Easy parallelization for ``Python`` jobs.

installation
============

Clone the repository and run ``./setup``. This will check if you have ``mpi4py`` installed -- this package is required for ``MPI`` parallelization on a cluster. It will also attempt to update your ``PATH`` and ``PYTHONPATH`` variables in ``~/.profile``, ``~/.bash_profile``, or ``~/.bashrc``.

examples
========

``para`` is really straightforward. On your computer, ``cd`` into the ``scripts/`` directory and type::

    python example.py

to run a very simple job in parallel using ``Python``'s ``multiprocessing`` module. If you wish to use ``para`` on a computer cluster with ``MPI``, run the same example using the ``mpi`` command::

    mpi example.py

This will generate a ``PBS`` script (type ``para -h`` to see available PBS options) and submit it to the queue using ``qsub``. Once the job is complete, the output is stored in ``mpi_example.py.log`` in the same directory.

using ``para`` in your project
==============================

If you want to parallelize a certain part of your code, you should have a script that looks something like this:

.. code-block:: python

    import para
    
    def func(x, *args, **kwargs):
        '''
        The function you wish to parallelize
  
        '''
        
        # Do some lengthy calculation
        
        return y
    
    # Call ``func()`` in parallel, once for each element in ``xlist``
    # and store the results in the list ``res``. The options ``args``
    # and ``kwargs`` are any arguments/keywords to be passed to ``func``
    
    res = para.map(func, xlist, args = (), kwargs = {}))

To run on a single node using ``multiprocessing``, execute the script with ``python``. Or, to run on multiple nodes with ``MPI``, execute the script with the ``mpi`` command. In the latter case, you can specify the number of nodes, the walltime, and several other PBS arguments. Just run ``mpi -h`` to see the complete list.

using ``para`` with ``emcee``
=============================

Since ``emcee`` maps each walker's position vector to your likelihood function once per step in the chain, you don't want all the overhead that comes with creating a new pool object every time you call ``para.map``. Instead, you should use the ``para.Pool`` object. See ``scripts/mcmc.py`` for an example.