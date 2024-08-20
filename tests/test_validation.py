#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Perform automated testing on pdvalidate.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     support@s3dev.uk

"""
# pylint: disable=import-error
# pylint: disable=protected-access
# pylint: disable=wrong-import-order
# pylint: disable=wrong-import-position

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
# Set sys.path for relative imports ^^^
import contextlib
import inspect
import io
import numpy as np
import pandas as pd
import pickle
from datetime import datetime as dt
# locals
from base import TestBase
from testlibs import msgs
from pdvalidate.validation import validate as pv
from pdvalidate.validation import ValidationWarning


class TestHelpers(TestBase):
    """Testing suite for the helper methods.

    A helper method is defined as any method which is *not* part of the
    core validation functionality:

        - validate_date
        - validate_numeric
        - validate_string
        - validate_timestamp

    """

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='Helper methods')

    def test01a__test_dtype_numeric(self):
        """Test the ``test_dtype_numeric`` method.

        :Test:
            - Verify the method returns the expected boolean value.

        """
        s1 = pd.Series([1, 2, 3.0])
        s2 = pd.Series([float('nan'), 2, 3.0])
        s3 = pd.Series([1, 2, '3.0'])
        s4 = pd.Series([1, 2, '3.0', True])
        for s, exp in zip([s1, s2, s3, s4], [True, True, False, False]):
            with self.subTest():
                tst = pv.test_dtype_numeric(series=s)
                self.assertEqual(exp, tst)

    def test02a__test_dtype_object(self):
        """Test the ``test_dtype_object`` method.

        :Test:
            - Verify the method returns the expected boolean value.

        """
        s1 = pd.Series(['a', 'b', 'c'])
        s2 = pd.Series(['a', '1', '2.0'])
        s3 = pd.Series([1, '1', '2.0', False])
        s4 = pd.Series([1, 2, 3, 4.0, True])
        s5 = pd.Series([1, 2, 3, 4.0, 5])
        for s, exp in zip([s1, s2, s3, s4, s5], [True, True, True, True, False]):
            with self.subTest():
                tst = pv.test_dtype_object(series=s)
                self.assertEqual(exp, tst)

    def test03a___get_return_object__mask_series(self):
        """Test the ``_get_return_object`` method for 'mask_series'.

        :Test:
            - Verify the method returns the expected masked value.

        """
        strings = pd.Series(['1', '1', 'ab\n', 'a b', 'Ab', 'AB', np.nan])
        masks = [pd.Series([False, False, False, True, True, False, False]),
                 pd.Series([True, True, False, True, True, False, True])]
        exp = pd.Series([True, True, False, True, True, False, True])
        tst = pv._get_return_object(masks=masks, values=strings, return_type='mask_series')
        self.assertTrue(exp.equals(tst), msg=self._MSG1.format(exp, tst))

    def test03b___get_return_object__mask_frame(self):
        """Test the ``_get_return_object`` method for 'mask_frame'.

        :Test:
            - Verify the method returns the expected masked value.

        """
        strings = pd.Series(['1', '1', 'ab\n', 'a b', 'Ab', 'AB', np.nan])
        masks = [pd.Series([False, False, False, True, True, False, False]),
                 pd.Series([True, True, False, True, True, False, True])]
        exp = pd.concat(masks, axis=1)
        tst = pv._get_return_object(masks=masks, values=strings, return_type='mask_frame')
        self.assertTrue(exp.equals(tst), msg=self._MSG1.format(exp, tst))

    def test03c___get_return_object__values(self):
        """Test the ``_get_return_object`` method for 'values'.

        :Test:
            - Verify the method returns the expected masked value.

        """
        strings = pd.Series(['1', '1', 'ab\n', 'a b', 'Ab', 'AB', np.nan])
        masks = [pd.Series([False, False, False, True, True, False, False]),
                 pd.Series([True, True, False, True, True, False, True])]
        exp = pd.Series([np.nan, np.nan, 'ab\n', np.nan, np.nan, 'AB', np.nan])
        tst = pv._get_return_object(masks=masks, values=strings, return_type='values')
        self.assertTrue(exp.equals(tst), msg=self._MSG1.format(exp, tst))

    def test03d___get_return_object__invalid(self):
        """Test the ``_get_return_object`` method for an invalid type.

        :Test:
            - Verify the method raises a ValueError.

        """
        strings = pd.Series(['1', '1'])
        masks = [pd.Series([False, False])]
        with self.assertRaises(ValueError):
            pv._get_return_object(masks=masks, values=strings, return_type='something invalid')

    def test04a__mask_nonconvertible__datetime(self):
        """Test the ``mask_nonconvertible`` method for a datetime type.

        :Test:
            - Verify the method returns the expected mask Series.

        """
        mixed = pd.Series([1, 2.3, np.nan, 'abc', dt(2014, 1, 7), '2014', '2024-08', '2024-08-23'])
        exp = pd.Series([True, True, False, True, False, True, False, False])
        tst = pv.mask_nonconvertible(series=mixed,
                                     to_datatype='datetime',
                                     datetime_format='%Y-%m',
                                     exact_date=False)
        self.assertTrue(exp.equals(tst))

    def test04b__mask_nonconvertible__datetime_exact(self):
        """Test the ``mask_nonconvertible`` method for a datetime type,
        with exact format matching.

        :Test:
            - Verify the method returns the expected mask Series.

        """
        mixed = pd.Series([1, 2.3, np.nan, 'abc', dt(2014, 1, 7), '2014', '2024-08', '2024-08-23'])
        exp = pd.Series([True, True, False, True, False, True, False, True])
        tst = pv.mask_nonconvertible(series=mixed,
                                     to_datatype='datetime',
                                     datetime_format='%Y-%m',
                                     exact_date=True)
        self.assertTrue(exp.equals(tst))

    def test04c__mask_nonconvertible__numeric(self):
        """Test the ``mask_nonconvertible`` method for a numeric type.

        :Test:
            - Verify the method returns the expected mask Series.

        """
        mixed = pd.Series([1, 2.3, np.nan, 'abc', dt(2014, 1, 7), '2014', '2024-08'])
        exp = pd.Series([False, False, False, True, True, False, True])
        tst = pv.mask_nonconvertible(series=mixed, to_datatype='numeric')
        self.assertTrue(exp.equals(tst))

    def test04d__mask_nonconvertible__invalid(self):
        """Test the ``mask_nonconvertible`` method for an invalid type.

        :Test:
            - Verify the method raises a ValueError.

        """
        mixed = pd.Series(['1', 2.3])
        with self.assertRaises(ValueError):
            pv.mask_nonconvertible(series=mixed, to_datatype='something invalid')

    def test05a__to_datetime(self):
        """Test the ``to_datetime`` method.

        :Test:
            - Verify the method returns the expected mask Series.

        """
        mixed = pd.Series([1, 2.3, np.nan, 'abc', dt(2014, 1, 7), '2014', '2024-08', '2024-08-23'])
        exp = [pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.Timestamp('2014-01-07 00:00:00'),
               pd.NaT, pd.Timestamp('2024-08-01 00:00:00'), pd.Timestamp('2024-08-01 00:00:00')]
        with self.assertWarns(ValidationWarning):
            tst = pv.to_datetime(arg=mixed, datetime_format='%Y-%m', exact=False)
        self.assertTrue(exp == tst.tolist())

    def test05b__to_datetime__exact(self):
        """Test the ``to_datetime`` method for an extact date format.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the call raises (warns about) a ValidationWarning.

        """
        mixed = pd.Series([1, 2.3, np.nan, 'abc', dt(2014, 1, 7), '2014', '2024-08', '2024-08-23'])
        exp = [pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.Timestamp('2014-01-07 00:00:00'),
               pd.NaT, pd.Timestamp('2024-08-01 00:00:00'), pd.NaT]
        with self.assertWarns(ValidationWarning):
            tst = pv.to_datetime(arg=mixed, datetime_format='%Y-%m', exact=True)
        self.assertTrue(exp == tst.tolist())

    def test05c__to_datetime__list(self):
        """Test the ``to_datetime`` method for a list of datetimes.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the call raises (warns about) a ValidationWarning.

        """
        mixed = [1, 2.3, np.nan, 'abc', dt(2014, 1, 7), '2014', '2024-08', '2024-08-23']
        exp = [pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.Timestamp('2014-01-07 00:00:00'),
               pd.NaT, pd.Timestamp('2024-08-01 00:00:00'), pd.NaT]
        with self.assertWarns(ValidationWarning):
            tst = pv.to_datetime(arg=mixed, datetime_format='%Y-%m', exact=True)
        self.assertTrue(exp == tst.tolist())

    def test06a__to_numeric(self):
        """Test the ``to_numeric`` method.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the call raises (warns about) a ValidationWarning.

        """
        mixed = pd.Series([1, 2.3, np.nan, 'abc', dt(2014, 1, 7), '2014', '2024-08', '2024-08-23'])
        exp = pd.Series([1.0, 2.3, float('nan'), float('nan'), float('nan'),
                         2014.0, float('nan'), float('nan')])
        with self.assertWarns(ValidationWarning):
            tst = pv.to_numeric(arg=mixed)
        self.assertTrue(exp.equals(tst))

    def test06b__to_numeric__list(self):
        """Test the ``to_numeric`` method for a list of numeric values.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the call raises (warns about) a ValidationWarning.

        """
        mixed = [1, 2.3, np.nan, 'abc', dt(2014, 1, 7), '2014', '2024-08', '2024-08-23']
        with self.assertWarns(ValidationWarning):
            tst = pv.to_numeric(arg=mixed)
        self.assertTrue(tst[~np.isnan(tst)].sum() == 2017.3)

    def test07a__to_string(self):
        """Test the ``to_string`` method.

        :Test:
            - Verify the method returns the expected mask Series.

        """
        mixed = pd.Series([1, 2.3, 'abc', dt(2014, 1, 7), 2014, pd.Timestamp('2024-08'),
                           '2024-08-23'])
        exp = pd.Series(['1', '2.3', 'abc', '2014-01-07', '2014', '2024-08-01', '2024-08-23'])
        tst = pv.to_string(series=mixed, float_format='%g')
        self.assertTrue(exp.equals(tst))

    def test07b__to_string__numeric(self):
        """Test the ``to_string`` method for numeric types.

        :Test:
            - Verify the method returns the expected mask Series.

        """
        mixed = pd.Series([1, 2.3, '4.567', 89.012, np.nan, float('nan')])
        exp = pd.Series(['1', '2.3', '4.567', '89.012', np.nan, float('nan')])
        tst = pv.to_string(series=mixed, float_format='%g')
        for exp_, tst_ in zip(exp, tst):
            with self.subTest(msg=f'{exp_=} {tst_=}'):
                if isinstance(tst_, float):
                    # NaN cannot use the '==' operator.
                    self.assertTrue(np.isnan(tst_))
                else:
                    self.assertEqual(exp_, tst_)

    def test07c__to_string__datetime(self):
        """Test the ``to_string`` method for datetime types.

        :Test:
            - Verify the method returns the expected mask Series.

        """
        mixed = pd.Series([dt(2014, 1, 7), 2014, pd.Timestamp('2024-08'), '2024-08-23'])
        exp = pd.Series(['2014-01', '2014', '2024-08', '2024-08-23'])
        tst = pv.to_string(series=mixed, datetime_format='%Y-%m')
        self.assertTrue(exp.equals(tst))


class TestValidators(TestBase):
    """Testing suite for the core validation methods.

    A validation method is defined as any method which is part of the
    core validation functionality:

        - validate_date
        - validate_numeric
        - validate_string
        - validate_timestamp

    """

    _FILE = os.path.splitext(os.path.basename(__file__))[0]

    _DIR_VER_DATA = os.path.join(TestBase._DIR_VER_DATA, _FILE)
    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='Validation methods')

    def test01a__validate_date(self):
        """Test the ``validate_date`` method.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the correct RangeWarning is displayed.

        """
        buf = io.StringIO()
        msgexp = ('[RangeWarning]: \'DateTest\': NaT value(s); duplicates; '
                  'date(s) too early; date(s) too late.')
        exp = None
                                                                # Parameter addressed:
        s1 = pd.Series([dt(2010, 10, 7),                        # min_date
                        dt(2014, 8, 13),                        # OK
                        pd.Timestamp('2014-08-13'),             # unique
                        pd.Timestamp('2018-03-15'),             # max_date
                        np.nan],                                # nullable
                        name='DateTest')
        with contextlib.redirect_stdout(buf):
            tst = pv.validate_date(s1,
                                   nullable=False,
                                   unique=True,
                                   min_date=dt(2013, 1, 1),
                                   max_date=dt(2015, 12, 31),
                                   return_type=None)
        msg = ''.join(self.strip_ansi_colour(buf.getvalue())).strip()
        self.assertEqual(exp, tst)
        self.assertEqual(msg, msgexp)

    def test01b__validate_date__values(self):
        """Test the ``validate_date`` method; return_type='values'.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the correct RangeWarning is displayed.

        """
        buf = io.StringIO()
        msgexp = ('[RangeWarning]: \'DateTest\': NaT value(s); duplicates; '
                  'date(s) too early; date(s) too late.')
        exp = (pd.Series([pd.NaT, dt(2014, 8, 13), dt(2015, 12, 31), dt(2014, 2, 2),
                          pd.NaT, pd.NaT, pd.NaT]),
               msgexp)
                                                                # Parameter addressed:
        s1 = pd.Series([dt(2010, 10, 7),                        # min_date
                        dt(2014, 8, 13),                        # OK
                        dt(2015, 12, 31),                       # OK
                        '2014-02-02',                           # convert, dateformat (OK)
                        pd.Timestamp('2014-08-13'),             # unique
                        pd.Timestamp('2018-03-15'),             # max_date
                        np.nan],                                # nullable
                        name='DateTest')
        with contextlib.redirect_stdout(buf):
            tst = pv.validate_date(s1,
                                   convert=True,
                                   dateformat='%Y-%m-%d',
                                   nullable=False,
                                   unique=True,
                                   min_date=dt(2013, 1, 1),
                                   max_date=dt(2015, 12, 31),
                                   return_type='values')
        msg = ''.join(self.strip_ansi_colour(buf.getvalue())).strip()
        self.assertTrue(exp[0].equals(tst[0]))  # Series
        self.assertEqual(tst[1], msgexp)        # Message from return value.
        self.assertEqual(msg, msgexp)           # Message from terminal

    def test01c__validate_date__mask_frame(self):
        """Test the ``validate_date`` method; return_type='mask_frame'.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the correct RangeWarning is displayed.

        """
        me = inspect.stack()[0].function
        buf = io.StringIO()
                                                                # Parameter addressed:
        s1 = pd.Series([dt(2010, 10, 7),                        # min_date
                        dt(2014, 8, 13),                        # OK
                        dt(2015, 12, 31),                       # OK
                        '2014-02-02',                           # convert, dateformat (OK)
                        pd.Timestamp('2014-08-13'),             # unique
                        pd.Timestamp('2018-03-15'),             # max_date
                        np.nan],                                # nullable
                        name='DateTest')
        with contextlib.redirect_stdout(buf):
            tst = pv.validate_date(s1,
                                   convert=True,
                                   dateformat='%Y-%m-%d',
                                   nullable=False,
                                   unique=True,
                                   min_date=dt(2013, 1, 1),
                                   max_date=dt(2015, 12, 31),
                                   return_type='mask_frame')
        with open(os.path.join(self._DIR_VER_DATA, f'{me}.p'), 'rb') as f:
            exp = pickle.load(f)
        msg = ''.join(self.strip_ansi_colour(buf.getvalue())).strip()
        self.assertTrue(exp[0].equals(tst[0]))  # Series
        self.assertEqual(tst[1], exp[1])        # Message from return value.
        self.assertEqual(msg, exp[1])           # Message from terminal

    def test01d__validate_date__mask_series(self):
        """Test the ``validate_date`` method; return_type='mask_series'.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the correct RangeWarning is displayed.

        """
        me = inspect.stack()[0].function
        buf = io.StringIO()
                                                                # Parameter addressed:
        s1 = pd.Series([dt(2010, 10, 7),                        # min_date
                        dt(2014, 8, 13),                        # OK
                        dt(2015, 12, 31),                       # OK
                        '2014-02-02',                           # convert, dateformat (OK)
                        pd.Timestamp('2014-08-13'),             # unique
                        pd.Timestamp('2018-03-15'),             # max_date
                        np.nan],                                # nullable
                        name='DateTest')
        with contextlib.redirect_stdout(buf):
            tst = pv.validate_date(s1,
                                   convert=True,
                                   dateformat='%Y-%m-%d',
                                   nullable=False,
                                   unique=True,
                                   min_date=dt(2013, 1, 1),
                                   max_date=dt(2015, 12, 31),
                                   return_type='mask_series')
        with open(os.path.join(self._DIR_VER_DATA, f'{me}.p'), 'rb') as f:
            exp = pickle.load(f)
        msg = ''.join(self.strip_ansi_colour(buf.getvalue())).strip()
        self.assertTrue(exp[0].equals(tst[0]))  # Series
        self.assertEqual(tst[1], exp[1])        # Message from return value.
        self.assertEqual(msg, exp[1])           # Message from terminal

    def test02a__validate_numeric(self):
        """Test the ``validate_numeric`` method.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the correct RangeWarning is displayed.

        """
        buf = io.StringIO()
        msgexp = ('[RangeWarning]: \'NumericTest\': NaN value(s); duplicates; '
                  'non-integer(s); value(s) too low.')
        exp = None
                                                # Parameter addressed:
        s2 = pd.Series([13,                     # min_value
                        42,                     # OK
                        73,                     # OK
                        73,                     # unique
                        3.14159,                # integer
                        1.1618033,              # integer
                        np.nan,                 # nullable
                        float('nan')],          # nullable
                       name='NumericTest')
        with contextlib.redirect_stdout(buf):
            tst = pv.validate_numeric(s2,
                                      nullable=False,
                                      unique=True,
                                      integer=True,
                                      min_value=15,
                                      max_value=100,
                                      return_type=None)
        msg = ''.join(self.strip_ansi_colour(buf.getvalue())).strip()
        self.assertEqual(exp, tst)
        self.assertEqual(msg, msgexp)

    def test02b__validate_numeric__values(self):
        """Test the ``validate_numeric`` method; return_type='values'.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the correct RangeWarning is displayed.

        """
        buf = io.StringIO()
        msgexp = ('[RangeWarning]: \'NumericTest\': NaN value(s); duplicates; '
                  'non-integer(s); value(s) too low.')
        exp = (pd.Series([np.nan, 42.0, 73.0, np.nan, np.nan, np.nan, np.nan, np.nan]),
               msgexp)
                                                # Parameter addressed:
        s2 = pd.Series([13,                     # min_value
                        42,                     # OK
                        73,                     # OK
                        73,                     # unique
                        3.14159,                # integer
                        1.1618033,              # integer
                        np.nan,                 # nullable
                        float('nan')],          # nullable
                       name='NumericTest')
        with contextlib.redirect_stdout(buf):
            tst = pv.validate_numeric(s2,
                                      nullable=False,
                                      unique=True,
                                      integer=True,
                                      min_value=15,
                                      max_value=100,
                                      return_type='values')
        msg = ''.join(self.strip_ansi_colour(buf.getvalue())).strip()
        self.assertTrue(exp[0].equals(tst[0]))  # Series
        self.assertEqual(tst[1], msgexp)        # Message from return value.
        self.assertEqual(msg, msgexp)           # Message from terminal

    def test02c__validate_numeric__non_numeric(self):
        """Test the ``validate_numeric`` method, with a single
        non-numeric value.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the correct DatatypeWarning is displayed.

        """
        buf = io.StringIO()
        msgexp = ('[DatatypeWarning]: \'NumericTest\': Expected numeric, received object. '
                  'Please address and re-validate.')
                                                # Parameter addressed:
        s2 = pd.Series([13,                     # min_value
                        'a',                    # Non-numeric to trigger warning.
                        42],                    # OK
                       name='NumericTest')
        with contextlib.redirect_stdout(buf):
            _ = pv.validate_numeric(s2,
                                    nullable=False,
                                    unique=True,
                                    integer=True,
                                    min_value=15,
                                    max_value=100,
                                    return_type=None)
        msg = ''.join(self.strip_ansi_colour(buf.getvalue())).strip()
        self.assertEqual(msg, msgexp)           # Message from terminal

    def test03a__validate_string__mask_series(self):
        """Test the ``validate_string`` method.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the correct RangeWarning is displayed.

        """
        me = inspect.stack()[0].function
        buf = io.StringIO()
        s3 = pd.Series([                    # Parameter addressed:
                        float('nan'),       # nullable
                        np.nan,             # nullable
                        '1',                # min_length
                        '12345678901',      # max_length
                        'CaseTEST',         # case
                        'casetest',         # case (OK)
                        'ab\nab',           # newlines
                        'abab\n',           # trailing_newlines
                        'abc abc',          # whitespace
                        ' abcabc ',         # whitespace
                        'goodstring',       # matching_regex (OK)
                        'badstring',        # non_matching_regex (OK)
                        'whitelist',        # whitelist
                        'blacklist',        # blacklist
                        'goodstring',       # unique
                        b'abcd',            # Invalid type
                        0xc0ffee,           # Invalid type
                        123456,             # Invalid type
                        123.456,            # Invalid type
                        'abc 123',          # Includes whitespace
                        'abc123',           # OK
                        'accepted',         # OK
                        'helloworld',       # OK
                       ],
                       name='StringTest')
        with contextlib.redirect_stdout(buf):
            tst = pv.validate_string(s3,
                                     nullable=True,
                                     unique=True,
                                     min_length=2,
                                     max_length=10,
                                     case='lower',
                                     newlines=False,
                                     trailing_whitespace=True,
                                     whitespace=False,
                                     matching_regex=None,
                                     non_matching_regex=None,
                                     whitelist=None,
                                     blacklist=['blacklist', 'blocked', 'ignore'],
                                     return_type='mask_series')
        with open(os.path.join(self._DIR_VER_DATA, f'{me}.p'), 'rb') as f:
            exp = pickle.load(f)
        msg = ''.join(self.strip_ansi_colour(buf.getvalue())).strip()
        self.assertTrue(exp[0].equals(tst[0]))  # Series
        self.assertEqual(tst[1], exp[1])        # Message from return value.
        self.assertEqual(msg, exp[1])           # Message from terminal

    def test03b__validate_string__mask_series__whitelist(self):
        """Test the ``validate_string`` method with a whitelist.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the correct RangeWarning is displayed.

        """
        me = inspect.stack()[0].function
        buf = io.StringIO()
        s3 = pd.Series([                    # Parameter addressed:
                        float('nan'),       # nullable
                        np.nan,             # nullable
                        '1',                # min_length
                        '12345678901',      # max_length
                        'CaseTEST',         # case
                        'casetest',         # case (OK)
                        'ab\nab',           # newlines
                        'abab\n',           # trailing_newlines
                        'abc abc',          # whitespace
                        ' abcabc ',         # whitespace
                        'goodstring',       # matching_regex (OK)
                        'badstring',        # non_matching_regex (OK)
                        'whitelist',        # whitelist
                        'blacklist',        # blacklist
                        'goodstring',       # unique
                        b'abcd',            # Invalid type
                        0xc0ffee,           # Invalid type
                        123456,             # Invalid type
                        123.456,            # Invalid type
                        'abc 123',          # Includes whitespace
                        'abc123',           # OK
                        'accepted',         # OK
                        'helloworld',       # OK
                       ],
                       name='StringTest')
        with contextlib.redirect_stdout(buf):
            tst = pv.validate_string(s3,
                                     nullable=True,
                                     unique=True,
                                     min_length=2,
                                     max_length=10,
                                     case='lower',
                                     newlines=False,
                                     trailing_whitespace=True,
                                     whitespace=False,
                                     matching_regex=None,
                                     non_matching_regex=None,
                                     whitelist=['whitelist', 'goodstring'],
                                     blacklist=['blacklist', 'blocked', 'ignore'],
                                     return_type='mask_series')
        with open(os.path.join(self._DIR_VER_DATA, f'{me}.p'), 'rb') as f:
            exp = pickle.load(f)
        msg = ''.join(self.strip_ansi_colour(buf.getvalue())).strip()
        self.assertTrue(exp[0].equals(tst[0]))  # Series
        self.assertEqual(tst[1], exp[1])        # Message from return value.
        self.assertEqual(msg, exp[1])           # Message from terminal

    def test03c__validate_string__mask_series__matching_regex(self):
        """Test the ``validate_string`` method with a matching regex
        pattern.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the correct RangeWarning is displayed.

        """
        me = inspect.stack()[0].function
        buf = io.StringIO()
        s3 = pd.Series([                    # Parameter addressed:
                        float('nan'),       # nullable
                        np.nan,             # nullable
                        '1',                # min_length
                        '12345678901',      # max_length
                        'CaseTEST',         # case
                        'casetest',         # case (OK)
                        'ab\nab',           # newlines
                        'abab\n',           # trailing_newlines
                        'abc abc',          # whitespace
                        ' abcabc ',         # whitespace
                        'goodstring',       # matching_regex (OK)
                        'badstring',        # non_matching_regex (OK)
                        'whitelist',        # whitelist
                        'blacklist',        # blacklist
                        'goodstring',       # unique
                        b'abcd',            # Invalid type
                        0xc0ffee,           # Invalid type
                        123456,             # Invalid type
                        123.456,            # Invalid type
                        'abc 123',          # Includes whitespace
                        'abc123',           # OK
                        'accepted',         # OK
                        'helloworld',       # OK
                       ],
                       name='StringTest')
        with contextlib.redirect_stdout(buf):
            tst = pv.validate_string(s3,
                                     nullable=True,
                                     unique=True,
                                     min_length=2,
                                     max_length=10,
                                     case='lower',
                                     newlines=False,
                                     trailing_whitespace=True,
                                     whitespace=False,
                                     matching_regex='^[a-z]+string$',
                                     non_matching_regex=None,
                                     whitelist=None,
                                     blacklist=None,
                                     return_type='mask_series')
        with open(os.path.join(self._DIR_VER_DATA, f'{me}.p'), 'rb') as f:
            exp = pickle.load(f)
        msg = ''.join(self.strip_ansi_colour(buf.getvalue())).strip()
        self.assertTrue(exp[0].equals(tst[0]))  # Series
        self.assertEqual(tst[1], exp[1])        # Message from return value.
        self.assertEqual(msg, exp[1])           # Message from terminal

    def test03d__validate_string__mask_series__non_matching_regex(self):
        """Test the ``validate_string`` method with a non-matching regex
        pattern.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the correct RangeWarning is displayed.

        """
        me = inspect.stack()[0].function
        buf = io.StringIO()
        s3 = pd.Series([                    # Parameter addressed:
                        float('nan'),       # nullable
                        np.nan,             # nullable
                        '1',                # min_length
                        '12345678901',      # max_length
                        'CaseTEST',         # case
                        'casetest',         # case (OK)
                        'ab\nab',           # newlines
                        'abab ',            # trailing_whitespace
                        'abc abc',          # whitespace
                        ' abcabc ',         # whitespace
                        'goodstring',       # matching_regex (OK)
                        'badstring',        # non_matching_regex (OK)
                        'whitelist',        # whitelist
                        'blacklist',        # blacklist
                        'goodstring',       # unique
                        b'abcd',            # Invalid type
                        0xc0ffee,           # Invalid type
                        123456,             # Invalid type
                        123.456,            # Invalid type
                        'abc 123',          # Includes whitespace
                        'abc123',           # OK
                        'accepted',         # OK
                        'helloworld',       # OK
                       ],
                       name='StringTest')
        with contextlib.redirect_stdout(buf):
            tst = pv.validate_string(s3,
                                     nullable=False,
                                     unique=True,
                                     min_length=2,
                                     max_length=10,
                                     case='lower',
                                     newlines=False,
                                     trailing_whitespace=False,
                                     whitespace=True,
                                     matching_regex=None,
                                     non_matching_regex='.*string.*',
                                     whitelist=None,
                                     blacklist=None,
                                     return_type='mask_series')
        with open(os.path.join(self._DIR_VER_DATA, f'{me}.p'), 'rb') as f:
            exp = pickle.load(f)
        msg = ''.join(self.strip_ansi_colour(buf.getvalue())).strip()
        self.assertTrue(exp[0].equals(tst[0]))  # Series
        self.assertEqual(tst[1], exp[1])        # Message from return value.
        self.assertEqual(msg, exp[1])           # Message from terminal

    def test03e__validate_string__non_string(self):
        """Test the ``validate_string`` method with a non-string value.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the correct DatatypeWarning is displayed.

        """
        buf = io.StringIO()
        s3 = pd.Series([1, 1.123, 73], name='StringTest')  # Non-string values to trigger warning.
        with contextlib.redirect_stdout(buf):
            _ = pv.validate_string(s3)
        msg = ''.join(self.strip_ansi_colour(buf.getvalue())).strip()
        msgexp = ('[DatatypeWarning]: StringTest: Expected object, received float64. '
                  'Please address and re-validate.')
        self.assertEqual(msg,  msgexp)

    def test04a__validate_timestamp(self):
        """Test the ``validate_timestamp`` method.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the correct RangeWarning is displayed.

        """
        me = inspect.stack()[0].function
        buf = io.StringIO()
        s4 = pd.Series([                                # Parameter addressed:
                        dt(2010, 10, 7),                # min_date
                        dt(2014, 8, 13),                # OK
                        pd.Timestamp('2014-08-13'),     # unique
                        pd.Timestamp('2018-03-15'),     # max_date
                        np.nan,                         # nullable
                       ],
                       name='DateTest')
        with contextlib.redirect_stdout(buf):
            tst = pv.validate_timestamp(s4,
                                        nullable=False,
                                        unique=True,
                                        min_timestamp=dt(2013, 1, 1),
                                        max_timestamp=dt(2015, 12, 31),
                                        return_type='mask_series')
        with open(os.path.join(self._DIR_VER_DATA, f'{me}.p'), 'rb') as f:
            exp = pickle.load(f)
        msg = ''.join(self.strip_ansi_colour(buf.getvalue())).strip()
        self.assertTrue(exp[0].equals(tst[0]))  # Series
        self.assertEqual(tst[1], exp[1])        # Message from return value.
        self.assertEqual(msg, exp[1])           # Message from terminal

    def test04b__validate_timestamp__non_unique(self):
        """Test the ``validate_timestamp`` method, with duplicate values.

        :Test:
            - Verify the method returns the expected mask Series.
            - Verify the correct RangeWarning is displayed.

        """
        me = inspect.stack()[0].function
        buf = io.StringIO()
        s4 = pd.Series([                                # Parameter addressed:
                        dt(2010, 10, 7),                # min_date
                        dt(2014, 8, 13),                # OK
                        pd.Timestamp('2014-08-13'),     # unique
                        pd.Timestamp('2018-03-15'),     # max_date
                        np.nan,                         # nullable
                       ],
                       name='DateTest')
        with contextlib.redirect_stdout(buf):
            tst = pv.validate_timestamp(s4,
                                        nullable=True,
                                        unique=False,
                                        min_timestamp=dt(2013, 1, 1),
                                        max_timestamp=dt(2015, 12, 31),
                                        return_type='mask_series')
        with open(os.path.join(self._DIR_VER_DATA, f'{me}.p'), 'rb') as f:
            exp = pickle.load(f)
        msg = ''.join(self.strip_ansi_colour(buf.getvalue())).strip()
        self.assertTrue(exp[0].equals(tst[0]))  # Series
        self.assertEqual(tst[1], exp[1])        # Message from return value.
        self.assertEqual(msg, exp[1])           # Message from terminal
