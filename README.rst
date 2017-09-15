pandas-validation
=================

pandas-validation is a small Python library for validating data
with the Python package `pandas <http://pandas.pydata.org>`_.

Source repository: `<https://github.com/jmenglund/pandas-validation>`_

Documentation at `<http://pandas-validation.readthedocs.io>`_

.. image:: https://api.travis-ci.org/jmenglund/pandas-validation.svg?branch=master
    :target: https://travis-ci.org/jmenglund/pandas-validation
    :alt: Documentation Status

.. image:: https://codecov.io/gh/jmenglund/pandas-validation/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jmenglund/pandas-validation
    :alt: Code coverage

.. image:: http://pandas-validation.readthedocs.io/en/latest/?badge=latest
    :target: http://pandas-validation.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation status



Installation
------------

For most users, the easiest way is probably to install the latest version
hosted on `PyPI <https://pypi.python.org/>`_:

.. code-block:: bash

    $ pip install pandas-validation

The project is hosted at https://github.com/jmenglund/pandas-validation and
can also be installed using git:

.. code-block:: bash

    $ git clone https://github.com/jmenglund/pandas-validation.git
    $ cd pandas-validation
    $ python setup.py install


Running tests
-------------

Testing is carried out with `pytest <http://pytest.org>`_. The following
example shows how you can run the test suite and generate a coverage report
with `coverage <https://coverage.readthedocs.io/>`_:

.. code-block:: bash

    $ py.test -v --pep8 pandasvalidation.py
    $ coverage run -m py.test
    $ coverage report --include pandasvalidation.py -m


Build the documentation
-----------------------

The documentation can be built with `sphinx <http://www.sphinx-doc.org>`_:

.. code-block:: bash

    $ cd pandas-validation
    $ sphinx-build -b html ./docs/source ./docs/_build/html
