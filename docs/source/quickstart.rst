.. _quickstart-guide:

================
Quickstart Guide
================

This quickstart guide provides a brief introduction on how to use 
``pdvalidate``. The library contains four core functions that let you
validate values in a ``pandas.Series`` (i.e. a column in a 
``pandas.DataFrame``).

The examples below are designed to help you get started. If you want to
know more detail regarding the lower-level functionality, please have a
look at the :ref:`library-api`.

.. contents::
   :local:
   :depth: 1

The code examples below assume the following imports exist at the top of
the module:

.. code-block:: python

    import numpy as np
    import pandas as pd
    from pdvalidate.validation import validate as pv


.. _validate-dates:

Validate dates
==============

The first example shows how to validate a pandas Series with a few
dates specified with Python's ``datetime.date`` data type. Values of
other types are replaced with
`NaT <https://pandas.pydata.org/docs/reference/api/pandas.NaT.html>`_
("Not-A-Time") prior to the validation. Warnings then inform the user if
any of the values are invalid.

.. code-block:: python

    from datetime import datetime as dt

    s1 = pd.Series([dt(2010, 10, 7),
                    dt(2014, 8, 13),
                    dt(2018, 3, 15),
                    dt(2018, 3, 15),
                    np.nan],
                    name='DateTest')

    pv.validate_date(s1,
                     nullable=False,
                     unique=True,
                     min_date=dt(2013, 1, 1),
                     max_date=dt(2015, 12, 31),
                     return_type=None)

    # A warning is displayed:
    [RangeWarning]: 'DateTest': NaT value(s); duplicates; date(s) too early; date(s) too late.

Continuing with the example above, if the ``return_type`` parameter is set
to ``'values'``, a ``tuple`` is returned containing a pandas Series with
only the valid dates as the first element, and the warning message 
(if applicable) as the second element. The warning message can then be
passed to a validation reporter for logging.

.. code-block:: python

    values = pv.validate_date(s1,
                              nullable=False,
                              unique=True,
                              min_date=dt(2013, 1, 1),
                              max_date=dt(2015, 12, 31),
                              return_type='values')  # <-- Note the change here.

Returns the following two-element tuple::
    
    (0          NaT
     1   2014-08-13
     2          NaT
     3          NaT
     4          NaT
     Name: TestSeries, dtype: datetime64[ns],
     "[RangeWarning]: 'TestSeries': NaT value(s); duplicates; date(s) too early; date(s) too late.")


.. _validate-numbers:

Validate numeric values
=======================

Validation of numeric values (e.g. floats and integers) follows the
same general principles as the validation of dates and timestamps.
Non-numeric values are treated as ``NaN``, and warnings are issued to
indicate invalid values to the user.

.. code-block:: python
    
    s2 = pd.Series([13, 42, 73, 73, 3.14159, 1.1618033, np.nan],
                   name='NumericTest')

    pv.validate_numeric(s2,
                        nullable=False,
                        unique=True,
                        integer=True,
                        min_value=15,
                        max_value=100,
                        return_type=None)

    # A warning is displayed:
    [RangeWarning]: 'NumericTest': NaN value(s); duplicates; non-integer(s); value(s) too low.

Continuing with the example above, if the ``return_type`` parameter is set
to ``'mask_series'``, a ``tuple`` is returned containing a boolean pandas
Series mask with ``True`` indicating the rows which *failed* validation and 
``False`` indicating the rows which *passed* as the first element, and the 
warning message (if applicable) as the second element. The warning message
can then be passed to a validation reporter for logging.

.. code-block:: python

    values = pv.validate_numeric(s2,
                                 nullable=False,
                                 unique=True,
                                 integer=True,
                                 min_value=15,
                                 max_value=100,
                                 return_type='mask_series')  # <-- Note the change here.

Returns the following two-element tuple::

    (0     True
     1    False  # <-- Reminder: False indicates a validation *pass*
     2    False  # <--
     3     True
     4     True
     5     True
     6     True
     dtype: bool,
     "[RangeWarning]: 'NumericTest': NaN value(s); duplicates; non-integer(s); value(s) too low.")

.. note:: As the ``True`` / ``False`` (fail/pass) logic may seem 
          counterintuitive for some use cases, the Series can be inverted
          using the tilde ``~`` operator, as::

              ~values[0]

          Thus changing ``True`` to a validation *pass* and ``False`` to a
          validation *failure*.


.. _validate-strings:

Validate strings
================

String validation works in the same way as the other validations, but
concerns only strings. Values of other types, like numbers and
timestamps, are simply replaced with ``NaN`` values before the
validation takes place. 

.. code-block:: python

    s3 = pd.Series(['1',            # Too short
                    '',             # Empty
                    'ab\n',         # Newline character present
                    'abc',          # OK
                    'Abc',          # Includes upper case character(s)
                    'ABc',          # Includes upper case character(s)
                    b'abcd',        # Bytes (not string)
                    'abc 123',      # Includes whitespace
                    'abc123',       # OK
                    'abc123',       # Duplicate
                    'ABC123',       # Includes upper case character(s)
                    'abc123abc123', # Too long
                    123,            # Numberic
                    0xc0ffee,       # Bytes
                    np.nan],        # NaN
                   name='StringTest')
        
    pv.validate_string(s3,
                       nullable=True,
                       unique=True,
                       min_length=2,
                       max_length=8,
                       case='lower',
                       newlines=False,
                       whitespace=False,
                       return_type=None)

    # A warning is displayed:
    [RangeWarning]: 'StringTest': Non-string value(s) set as NaN; duplicates; string(s) too short; string(s) too long; wrong case letter(s); newline character(s); whitespace.

Continuing with the example above, if the ``return_type`` parameter is set
to ``'mask_frame'``, a ``tuple`` is returned containing a boolean pandas
DataFrame mask with ``True`` indicating the rows which *failed* validation and 
``False`` indicating the rows which *passed* as the first element, and the 
warning message (if applicable) as the second element. The warning message
can then be passed to a validation reporter for logging.

.. code-block:: python

    values = pv.validate_string(s3,
                                nullable=True,
                                unique=True,
                                min_length=2,
                                max_length=8,
                                case='lower',
                                newlines=False,
                                whitespace=False,
                                return_type='mask_frame')  # <-- Note the change here.

Returns the following two-element tuple::

    (    invalid_type  nonunique too_short too_long wrong_case newlines whitespace
     0          False      False      True    False      False    False      False
     1          False      False      True    False      False    False      False
     2          False      False     False    False      False     True       True
     3          False      False     False    False      False    False      False
     4          False      False     False    False       True    False      False
     5          False      False     False    False       True    False      False
     6           True      False       NaN      NaN        NaN      NaN        NaN
     7          False      False     False    False      False    False       True
     8          False      False     False    False      False    False      False
     9          False       True     False    False      False    False      False
     10         False      False     False    False       True    False      False
     11         False      False     False     True      False    False      False
     12          True      False       NaN      NaN        NaN      NaN        NaN
     13          True      False       NaN      NaN        NaN      NaN        NaN
     14         False      False       NaN      NaN        NaN      NaN        NaN,
     "[RangeWarning]: 'StringTest': Non-string value(s) set as NaN; duplicates; string(s) too short; string(s) too long; wrong case letter(s); newline character(s); whitespace.")


.. _validate-timestamps:

Validate timestamps
===================

Validation of timestamps works in the same way as date validation.
The major difference is that only values of type ``pandas.Timestamp``
are taken into account. Values of other types are replaced by ``NaT``.

.. code-block:: python


    from datetime import datetime as dt

    s4 = pd.Series([pd.Timestamp(2010, 1, 1, 12, 30, 0),                # Invalid: Out of range
                    pd.Timestamp(2014, 2, 1, 12, 30, 0),                # Valid
                    pd.Timestamp(2014, 2, 1, 12, 30, 0),                # Invalid: Duplicate
                    dt(2015, 3, 1, 12, 30, 0),                          # Invalid: Datetime object
                    pd.to_datetime(dt(2020, 4, 1)),                     # Valid
                    '2024-02-02',                                       # Invalid: String
                    pd.to_datetime('2024-03-01', format='%Y-%m-%d'),    # Valid
                    1234,                                               # Invalid: Integer
                    np.nan],                                            # Invalid: NaN
                   name='TimestampTest') 

    pv.validate_timestamp(s4,
                          nullable=False, 
                          unique=True,
                          min_timestamp=pd.Timestamp(2011, 1, 1),
                          max_timestamp=dt(2024, 12, 31),
                          return_type=None)  

    # A warning is displayed:
    # [RangeWarning]: 'TimestampTest': Value(s) not of type pandas.Timestamp set as NaT; NaT value(s); duplicates; timestamp(s) too early.

Continuing with the example above, if the ``return_type`` parameter is set
to ``'values'``, a ``tuple`` is returned containing a pandas Series with
only the valid timestamps as the first element, and the warning message 
(if applicable) as the second element. The warning message can then be
passed to a validation reporter for logging.

.. code-block:: python

    values = pv.validate_timestamp(s4,
                                   nullable=False, 
                                   unique=True,
                                   min_timestamp=pd.Timestamp(2011, 1, 1),
                                   max_timestamp=dt(2024, 12, 31),
                                   return_type='values')  # <-- Note the change here.

Returns the following two-element tuple::

    (0                   NaT
     1   2014-02-01 12:30:00
     2                   NaT
     3                   NaT
     4   2020-04-01 00:00:00
     5                   NaT
     6   2024-03-01 00:00:00
     7                   NaT
     8                   NaT
     Name: TimestampTest, dtype: datetime64[ns],
     "[RangeWarning]: 'TimestampTest': Value(s) not of type pandas.Timestamp set as NaT; NaT value(s); duplicates; timestamp(s) too early.")

Summary
=======
This simple guide is designed to get you up and running with 
``pdvalidate``. However, the :ref:`library-api` section provides a detailed
explanation for each validation method, along with a description for each
parameter.

.. _pandas-nat: https://pandas.pydata.org/docs/reference/api/pandas.NaT.html

