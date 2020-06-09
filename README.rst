pdvalidate
==========

|Build-Status| |Coverage-Status| |PyPI-Status| |Doc-Status| |License|


Introduction
------------

The ``pdvalidate`` package is a fork from ``pandas-validation`` (v0.5.0)
originally written by Markus Englund, and was enhanced to include 
additional functionality; specifically to return the validation error 
messages (from each test) to the caller for capture and logging purposes.

Great efforts have been made to retain the initial integrity of the 
original ``pandas-validation`` project, while adding some new features.
Additionally, the automated test suite has been maintained and updated
to test the new functionality.

Thank you Markus for your hard work on the **excellent** framework, and
for sharing it with us all!


Overview
--------

``pdvalidate`` is a small Python library for validating data with the 
Python package `pandas <http://pandas.pydata.org>`_.

Source repository: `<https://github.com/s3dev/pdvalidate>`_

Documentation at `<http://pdvalidate.readthedocs.io>`_


Installation
------------

For most users, the easiest way is to install the latest version hosted 
on `PyPI <https://pypi.python.org/>`_:

.. code-block::

    $ pip install pdvalidate

The project is hosted at https://github.com/s3dev/pdvalidate and can 
also be installed using git:

.. code-block::

    $ git clone https://github.com/s3dev/pdvalidate.git
    $ cd pdvalidate
    $ python setup.py install


Running the tests
-----------------

Testing is carried out with `pytest <https://docs.pytest.org/>`_:

.. code-block::

    $ pytest -v test_validation.py

Test coverage can be calculated with `Coverage.py
<https://coverage.readthedocs.io/>`_ using the following commands:

.. code-block::

    $ coverage run -m pytest
    $ coverage report -m validation.py

The code follow style conventions in `PEP8
<https://www.python.org/dev/peps/pep-0008/>`_, which can be checked
with `pylint <https://pylint.org>`_:

.. code-block::

    $ pylint ./pdvalidate/validation.py ./tests/test_validation.py setup.py


Building the documentation
--------------------------

The documentation can be built with `Sphinx <http://www.sphinx-doc.org>`_
and the `Read the Docs Sphinx Theme
<https://sphinx-rtd-theme.readthedocs.io>`_:

.. code-block::

    $ cd pdvalidation
    $ sphinx-build -b html ./docs/source ./docs/_build/html


License
-------

pdvalidate is distributed under the `MIT license
<https://opensource.org/licenses/MIT>`_.


Author
------

Markus Englund: original pandas-validation package
J. Berendt: pdvalidate (fork)


.. |Build-Status| image:: https://api.travis-ci.org/s3dev/pdvalidate.svg?branch=master
   :target: https://travis-ci.org/s3dev/pdvalidate
   :alt: Build status
.. |Coverage-Status| image:: https://codecov.io/gh/s3dev/pdvalidate/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/s3dev/pdvalidate
    :alt: Code coverage
.. |PyPI-Status| image:: https://img.shields.io/pypi/v/pdvalidate.svg
   :target: https://pypi.python.org/pypi/pdvalidate
   :alt: PyPI status
.. |Doc-Status| image:: https://readthedocs.org/projects/pdvalidate/badge/?version=latest
   :target: http://pdvalidate.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation status
.. |License| image:: https://img.shields.io/pypi/l/pdvalidate.svg
   :target: https://raw.githubusercontent.com/s3dev/pdvalidate/master/LICENSE.txt
   :alt: License
