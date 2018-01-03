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

Testing is carried out with `pytest <https://docs.pytest.org/>`_:

.. code-block::

    $ pytest -v test_pandasvalidation.py

Test coverage can be calculated with `Coverage.py
<https://coverage.readthedocs.io/>`_ using the following commands:

.. code-block::

    $ coverage run -m pytest
    $ coverage report -m pandasvalidation.py

The code follow style conventions in `PEP8
<https://www.python.org/dev/peps/pep-0008/>`_, which can be checked
with `pycodestyle <http://pycodestyle.pycqa.org>`_:

.. code-block::

    $ pycodestyle pandasvalidation.py test_pandasvalidation.py setup.py


Building the documentation
--------------------------

The documentation can be built with `Sphinx <http://www.sphinx-doc.org>`_
and the `Read the Docs Sphinx Theme
<https://sphinx-rtd-theme.readthedocs.io>`_:

.. code-block::

    $ cd pandas-validation
    $ sphinx-build -b html ./docs/source ./docs/_build/html


License
-------

pandas-validation is distributed under the `MIT license
<https://opensource.org/licenses/MIT>`_.


Author
------

Markus Englund, `orcid.org/0000-0003-1688-7112
<http://orcid.org/0000-0003-1688-7112>`_


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
