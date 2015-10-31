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

If you want to parallelize a certain part of your code with ``MPI``, you should have a script that looks something like this::

.. code-block:: python

    # MPI is a decorator that endows a function with a ``pool`` kwarg
    
    from para import MPI
    
    def do_something(x)
    
        # Do some expensive calculation here.
        
        return y
    
    @MPI()
    def my_function(xlist, pool = None):
    
        # The ``MPI`` decorator gives ``my_function()`` access to a ``pool``
        # kwarg. Here we send off each element in ``xlist`` individually 
        # as an argument to ``do_something()``, which is called in parallel
        
        for y in pool.map(do_something, xlist):
        
            # We're just going to print each result to the screen here
            print(y)

    if __name__ == '__main__':
    
        # Here we simply call ``my_function()`` if this file is run as a script
        
        my_function()
