pandas-validation
=================

|Build-Status| |Coverage-Status| |PyPI-Status| |Doc-Status| |License|

pandas-validation is a small Python library for validating data
with the Python package `pandas <http://pandas.pydata.org>`_.

Source repository: `<https://github.com/jmenglund/pandas-validation>`_

Documentation at `<http://pandas-validation.readthedocs.io>`_


Installation
------------

For most users, the easiest way is probably to install the latest version
hosted on `PyPI <https://pypi.python.org/>`_:

.. code-block::

    $ pip install pandas-validation

The project is hosted at https://github.com/jmenglund/pandas-validation and
can also be installed using git:

.. code-block::

    $ git clone https://github.com/jmenglund/pandas-validation.git
    $ cd pandas-validation
    $ python setup.py install


Running the tests
-----------------

Testing is carried out with `pytest <http://pytest.org>`_. The following
example shows how you can run the test suite and generate a coverage report
with `coverage <https://coverage.readthedocs.io/>`_:

.. code-block::

    $ py.test -v --pep8 pandasvalidation.py
    $ coverage run -m py.test
    $ coverage report --include pandasvalidation.py -m


Building the documentation
--------------------------

The documentation can be built with `Sphinx <http://www.sphinx-doc.org>`_:

.. code-block::

    $ cd pandas-validation
    $ sphinx-build -b html ./docs/source ./docs/_build/html


License
-------

pandas-validation is distributed under the `MIT license <https://opensource.org/licenses/MIT>`_.


Author
------

Markus Englund, `orcid.org/0000-0003-1688-7112 <http://orcid.org/0000-0003-1688-7112>`_


.. |Build-Status| image:: https://api.travis-ci.org/jmenglund/pandas-validation.svg?branch=master
   :target: https://travis-ci.org/jmenglund/pandas-validation
   :alt: Build status
.. |Coverage-Status| image:: https://codecov.io/gh/jmenglund/pandas-validation/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jmenglund/pandas-validation
    :alt: Code coverage
.. |PyPI-Status| image:: https://img.shields.io/pypi/v/pandas-validation.svg
   :target: https://pypi.python.org/pypi/pandas-validation
   :alt: PyPI status
.. |Doc-Status| image:: https://readthedocs.org/projects/pandas-validation/badge/?version=latest
   :target: http://pandas-validation.readthedocs.io/en/latest/?badge=latest
   :alt: Documentatio status
.. |License| image:: https://img.shields.io/pypi/l/pandas-validation.svg
   :target: https://raw.githubusercontent.com/jmenglund/pandas-validation/master/LICENSE.txt
   :alt: License
