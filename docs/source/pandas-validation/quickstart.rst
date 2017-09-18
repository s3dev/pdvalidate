.. py:currentmodule:: pandasvalidation

.. _quickstart:

Quickstart
==========

This guide gives you a brief introduction on how to use pandas-validation.
The library contains three core functions that let you validate values in a
pandas Series. The examples below will help you get started. If you want to
know more, I suggest that you have a look at the :ref:`API reference<api>`.

* :ref:`validate-dates`
* :ref:`validate-numbers`
* :ref:`validate-strings`


The code examples below assume that you first do the following imports:

.. code-block:: pycon

    >>> import numpy as np
    >>> import pandas as pd
    >>> import pandasvalidation as pv


.. _validate-dates:

Validate datetimes
------------------

Our first example shows how to validate a pandas Series with a few dates
entered as strings. The strings will be automatically converted to datetimes
before they are validated. Warnings will then be issued and inform the
user that some values are invalid. If `return_values` is set to ``True``, a
pandas Series will be returned with the values converted to the datetime
data type.


.. code-block:: pycon

    >>> s1 = pd.Series(
    ...     ['2014', '2014-01-07', '2014-02-28', np.nan],
    ...     name='My dates')
    >>> pv.validate_datetime(
    ...     s1,
    ...     nullable=False,
    ...     unique=True,
    ...     min_datetime='2014-01-05',
    ...     max_datetime='2014-02-15',
    ...     return_values=False)


.. _validate-numbers:

Validate numeric values
-----------------------

Validation of numeric values works similarly to validation of datetime values.
Like in the example above, warnings will indicate invalid values to the user.
If `return_values` is set to ``True``, a pandas Series will be returned with
the values converted to a numeric data type.

.. code-block:: pycon

    >>> s2 = pd.Series(
    ...     [1, '1', '2.3', np.nan],
    ...     name='My numeric values')
    >>> pv.validate_numeric(
    ...     s2,
    ...     nullable=False,
    ...     unique=True,
    ...     integer=True,
    ...     min_value=2,
    ...     max_value=2,
    ...     return_values=False)


.. _validate-strings:

Validate strings
----------------

String validation is similar to validation of numeric datetime or numeric
values. Under the hood, all non-string values are converted to strings and
warnings then issued if there are invalid values. If `return_values` is
set to ``True``, a pandas Series will be returned with the values rendered
as strings.

.. code-block:: pycon

    >>> s3 = pd.Series(
    ...     [1, 1, 'ab\n', 'a b', 'Ab', 'AB', np.nan],
    ...     name='My strings')
    >>> pv.validate_string(
    ...     s3,
    ...     nullable=False,
    ...     unique=True,
    ...     min_length=2,
    ...     max_length=2,
    ...     case='lower',
    ...     newlines=False,
    ...     trailing_whitespace=False,
    ...     whitespace=False,
    ...     return_values=False)
