pandas-validation
=================

pandas-validation is a small Python library for validating data
with the Python package `pandas <http://pandas.pydata.org>`_.

Source repository: `<https://github.com/jmenglund/pandas-validation>`_


Installation
------------

The project is hosted at https://github.com/jmenglund/pandas-validation and 
can be installed using git:

.. code-block:: console

    $ git clone https://github.com/jmenglund/pandas-validation.git
    $ cd pandas-validation
    $ python setup.py install


Runing tests
------------

Run tests with pytest:

.. code-block:: console
    $ cd pandas-validation
    $ py.test -v --cov-report term-missing --cov pandasvalidation.py


Build the documentation
-----------------------

The documentation can be built with sphinx:

.. code-block:: console
    $ cd pandas-validation
    $ sphinx-build -b html ./docs/source ./docs/_build/html
