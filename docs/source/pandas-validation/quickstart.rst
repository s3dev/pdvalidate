.. py:currentmodule:: pandasvalidation

.. _quickstart:

Quickstart
==========

This guide gives you a brief introduction on how to use
pandas-validation. The library contains four core functions that let
you validate values in a pandas Series (or a DataFrame column). The
examples below will help you get started. If you want to know more, I suggest that you have a look at the :ref:`API reference<api>`.

* :ref:`validate-dates`
* :ref:`validate-timestamps`
* :ref:`validate-numbers`
* :ref:`validate-strings`


The code examples below assume that you first do the following imports:

.. code-block:: pycon

    >>> import numpy as np
    >>> import pandas as pd
    >>> import pandasvalidation as pv


.. _validate-dates:

Validate dates
--------------

Our first example shows how to validate a pandas Series with a few
dates specified with Python's `datetime.date` data type. Values of
other types are replaced with ``NaT`` ("not a time") prior to the
validation. Warnings then inform the user if any of the values are
invalid. If `return_type` is set to ``values``, a pandas Series will
be returned with only the valid dates.


.. code-block:: pycon

    >>> from datetime import date
    >>> s1 = pd.Series(
    ...     [
                date(2010, 10, 7),
                date(2018, 3, 15),
                date(2018, 3, 15),
                np.nan
            ], name='My dates')
    >>> pv.validate_date(
    ...     s1,
    ...     nullable=False,
    ...     unique=True,
    ...     min_date=date(2014, 1, 5),
    ...     max_date=date(2015, 2, 15),
    ...     return_type=None)
    ValidationWarning: 'My dates': NaT value(s); duplicates; date(s) too early; date(s) too late.


.. _validate-timestamps:

Validate timestamps
-------------------

Validation of timestamps works in the same way as date validation.
The major difference is that only values of type `pandas.Timestamp`
are taken into account. Values of other types are replaced by ``NaT``.
If `return_type` is set to ``values``, a pandas Series will
be returned with only the valid timestamps.


.. code-block:: pycon

    >>> s2 = pd.Series( 
    ...     [ 
    ...         pd.Timestamp(2018, 2, 7, 12, 31, 0), 
    ...         pd.Timestamp(2018, 2, 7, 13, 6, 0), 
    ...         pd.Timestamp(2018, 2, 7, 13, 6, 0), 
    ...         np.nan 
    ...     ], name='My timestamps') 
    >>> pv.validate_timestamp( 
    ...     s2, 
    ...     nullable=False, 
    ...     unique=True, 
    ...     min_timestamp=pd.Timestamp(2014, 1, 5, 0, 0, 0), 
    ...     max_timestamp=pd.Timestamp(2018, 2, 7, 13, 0, 0), 
    ...     return_type=None)                              
    ValidationWarning: 'My timestamps': NaT value(s); duplicates; timestamp(s) too late.


.. _validate-numbers:

Validate numeric values
-----------------------

Validation of numeric values (e.g. floats and integers) follows the
same general principles as the validation of dates and timestamps.
Non-numeric values are treated as ``NaN``, and warnings are issued to
indicate invalid values to the user. If `return_type` is set to
``values``, a pandas Series will be returned with only the valid
numeric values.

.. note::
    Prior to version 0.5.0, some non-numeric data types were
    automatically converted numeric types before the validation.
    This was often convenient but could also lead to unexpected
    behaviour. The current implementation is cleaner and gives the
    user more control over the data types.

.. code-block:: pycon

    >>> s3 = pd.Series(
    ...     [1, 1, 2.3, np.nan],
    ...     name='My numeric values')
    >>> pv.validate_numeric(
    ...     s3,
    ...     nullable=False,
    ...     unique=True,
    ...     integer=True,
    ...     min_value=2,
    ...     max_value=2,
    ...     return_type=None)
    ValidationWarning: 'My numeric values': NaN value(s); duplicates; non-integer(s); value(s) too low; values(s) too high.


.. _validate-strings:

Validate strings
----------------

String validation works in the same way as the other validations, but
concerns only strings. Values of other types, like numbers and
timestamps, are simply replaced with ``NaN`` values before the
validation takes place. If `return_type` is set to ``values``, a
pandas Series will be returned with only the valid strings.

.. note::
    Prior to version 0.5.0, some non-string data types were
    automatically converted to strings before the validation. This
    was often convenient but could also lead to unexpected behaviour.
    The current implementation is cleaner and gives the user more
    control over the data types.


.. code-block:: pycon

    >>> s4 = pd.Series(
    ...     ['1', 'ab\n', 'Ab', 'AB', np.nan],
    ...     name='My strings')
    >>> pv.validate_string(
    ...     s4,
    ...     nullable=False,
    ...     unique=True,
    ...     min_length=2,
    ...     max_length=2,
    ...     case='lower',
    ...     newlines=False,
    ...     whitespace=False,
    ...     return_type=None)
    ValidationWarning: 'My strings': NaN value(s); string(s) too short; string(s) too long; wrong case letter(s); newline character(s); whitespace.
