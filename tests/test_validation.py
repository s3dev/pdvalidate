#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Perform automated testing on pdvalidate.

:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@s3dev.uk

"""
# pylint: disable=protected-access
# pylint: disable=wrong-import-order
# pylint: disable=wrong-import-position
# pylint: disable=import-error

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import datetime
import numpy as np
import pytest
import pandas as pd
from datetime import datetime as dt
from pandas.testing import assert_series_equal, assert_frame_equal
from pdvalidate.validation import ei
from pdvalidate.validation import validate as pdv
from pdvalidate.validation import ValidationWarning


class TestDtype:

    @staticmethod
    def test_dtype_numeric():
        assert (pdv.test_dtype_numeric(series=pd.Series([1, 2, 3.0])) is True)

        assert (pdv.test_dtype_numeric(series=pd.Series([float('nan'), 2, 3.0])) is True)

        assert (pdv.test_dtype_numeric(series=pd.Series([1, 2, '3.0'])) is False)

        assert (pdv.test_dtype_numeric(series=pd.Series([1, 2, '3.0', True])) is False)

    @staticmethod
    def test_dtype_object():
        assert (pdv.test_dtype_object(series=pd.Series(['a', 'b', 'c'])) is True)

        assert (pdv.test_dtype_object(series=pd.Series(['a', '1', '2.0'])) is True)

        assert (pdv.test_dtype_object(series=pd.Series([1, '1', '2.0', False])) is True)

        assert (pdv.test_dtype_object(series=pd.Series([1, 2, 3, 4.0, True])) is True)

        assert (pdv.test_dtype_object(series=pd.Series([1, 2, 3, 4.0, 5])) is False)


class TestReturnTypes():

    strings = pd.Series(['1', '1', 'ab\n', 'a b', 'Ab', 'AB', np.nan])
    masks = [pd.Series([False, False, False, True, True, False, False]),
             pd.Series([True, True, False, True, True, False, True])]

    def test_return_mask_series(self):
        assert_series_equal(pdv._get_return_object(self.masks, self.strings, 'mask_series'),
                            pd.Series([True, True, False, True, True, False, True]))

    def test_return_mask_frame(self):
        assert_frame_equal(pdv._get_return_object(self.masks, self.strings, 'mask_frame'),
                           pd.concat(self.masks, axis='columns'))

    def test_return_values(self):
        assert_series_equal(pdv._get_return_object(self.masks, self.strings, 'values'),
                            pd.Series([np.nan, np.nan, 'ab\n', np.nan, np.nan, 'AB', np.nan]))

    def test_wrong_return_type(self):
        with pytest.raises(ValueError):
            pdv._get_return_object(self.masks, self.strings, 'wrong return type')


class TestMaskNonconvertible():

    mixed = pd.Series([1, 2.3, np.nan, 'abc', dt(2014, 1, 7), '2014'])
    inconvertible_numeric = pd.Series([False, False, False, True, True, False])
    inconvertible_exact_dates = pd.Series([True, True, False, True, True, False])
    inconvertible_inexact_dates = pd.Series([True, True, False, True, False, False])

    def test_numeric(self):
        assert_series_equal(pdv.mask_nonconvertible(self.mixed, 'numeric'),
                            self.inconvertible_numeric)

    def test_datetime_exact_date(self):
        assert_series_equal(pdv.mask_nonconvertible(self.mixed,
                                                    'datetime',
                                                    datetime_format='%Y',
                                                    exact_date=True),
                            self.inconvertible_exact_dates)

        assert_series_equal(pdv.mask_nonconvertible(self.mixed,
                                                    'datetime',
                                                    datetime_format='%Y',
                                                    exact_date=False),
                            self.inconvertible_inexact_dates)


class TestToDatetime():

    mixed = pd.Series([1, 2.3, np.nan, 'abc', dt(2014, 1, 7), '2014'])

    def test_exact(self):
        expected_result1 = [pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT,
                            pd.Timestamp('2014-01-01 00:00:00')]
        assert (pdv.to_datetime(self.mixed,
                                datetime_format='%Y',
                                exact=True).tolist() == expected_result1)

        expected_result2 = [pd.NaT, pd.NaT, pd.NaT, pd.NaT,
                            pd.Timestamp('2014-01-07 00:00:00'),
                            pd.Timestamp('2014-01-01 00:00:00')]
        assert (pdv.to_datetime(self.mixed,
                                datetime_format='%Y/%m/%d',
                                exact=False).tolist() == expected_result2)


class TestToNumeric():

    mixed = pd.Series([1, 2.3, np.nan, 'abc', dt(2014, 1, 7), '2014'])

    def test_conversion(self):
        assert (pdv.to_numeric(self.mixed).sum() == 2017.3)
        pytest.warns(ValidationWarning, pdv.to_numeric, self.mixed)


class TestToString():

    mixed = pd.Series([1, 2.3, np.nan, 'abc', dt(2014, 1, 7)])
    numeric_as_strings = pd.Series(['1', '2.3', np.nan, 'abc', dt(2014, 1, 7)])
    datetimes_as_strings = pd.Series([1, 2.3, np.nan, 'abc', '2014-01-07'])
    all_values_as_strings = pd.Series(['1', '2.3', np.nan, 'abc', '2014-01-07'])

    def test_numeric_to_string(self):
        assert_series_equal(pdv._numeric_to_string(self.mixed),
                            self.numeric_as_strings)

    def test_datetime_to_string(self):
        assert_series_equal(pdv._datetime_to_string(self.mixed,
                                                    datetime_format='%Y-%m-%d'),
                            self.datetimes_as_strings)

    def test_to_string(self):
        assert_series_equal(pdv.to_string(self.mixed,
                                          float_format='%g',
                                          datetime_format='%Y-%m-%d'),
                            self.all_values_as_strings)


class TestValidateDate():

    dates = pd.Series([datetime.datetime(2014, 1, 7),
                       datetime.datetime(2014, 1, 7),
                       datetime.datetime(2014, 2, 28),
                       pd.NaT])
    rtype = 'mask_series'

    def test_validation(self):
        results, msg = pdv.validate_date(self.dates, return_type='values')
        assert_series_equal(self.dates, results)

        _, msg = pdv.validate_date(self.dates,
                                   nullable=False,
                                   return_type=self.rtype)
        assert ei.natv in msg

        _, msg = pdv.validate_date(self.dates,
                                   unique=True,
                                   return_type=self.rtype)
        assert ei.nonu in msg

        _, msg = pdv.validate_date(self.dates,
                                   min_date=datetime.date(2014, 1, 8),
                                   return_type=self.rtype)
        assert ei.elyd in msg

        _, msg = pdv.validate_date(self.dates,
                                   max_date=datetime.date(2014, 1, 8),
                                   return_type=self.rtype)
        assert ei.lted in msg


class TestValidateTimestamp():

    timestamps = pd.Series([pd.Timestamp(2014, 1, 7, 12, 0, 5),
                            pd.Timestamp(2014, 1, 7, 12, 0, 5),
                            pd.Timestamp(2014, 2, 28, 0, 0, 0),
                            pd.NaT])
    rtype = 'mask_series'

    def test_validation(self):
        results, msg = pdv.validate_timestamp(self.timestamps, return_type='values')
        assert_series_equal(self.timestamps, results)

        _, msg = pdv.validate_timestamp(self.timestamps, nullable=False, return_type=self.rtype)
        assert ei.natv in msg

        _, msg = pdv.validate_timestamp(self.timestamps, unique=True, return_type=self.rtype)
        assert ei.nonu in msg

        _, msg = pdv.validate_timestamp(self.timestamps,
                                        min_timestamp=pd.Timestamp(2014, 1, 8),
                                        return_type=self.rtype)
        assert ei.elyt in msg

        _, msg = pdv.validate_timestamp(self.timestamps,
                                        max_timestamp=pd.Timestamp(2014, 1, 8),
                                        return_type=self.rtype)
        assert ei.ltet in msg


class TestValidateNumber():

    numeric_with_string = pd.Series([-1, -1, 2.3, '1'])
    numeric = pd.Series([-1, -1, 2.3, np.nan])
    rtype = 'mask_series'

    def test_validation(self):
        results, msg = pdv.validate_numeric(self.numeric_with_string,
                                            return_type='values')
        assert_series_equal(results, self.numeric)

        _, msg = pdv.validate_numeric(self.numeric, nullable=False, return_type=self.rtype)
        assert ei.nanv in msg

        _, msg = pdv.validate_numeric(self.numeric, unique=True, return_type=self.rtype)
        assert ei.nonu in msg

        _, msg = pdv.validate_numeric(self.numeric, integer=True, return_type=self.rtype)
        assert ei.nint in msg

        _, msg = pdv.validate_numeric(self.numeric, min_value=0, return_type=self.rtype)
        assert ei.lowv in msg

        _, msg = pdv.validate_numeric(self.numeric, max_value=0, return_type=self.rtype)
        assert ei.hghv in msg


class TestValidateString():

    mixed = pd.Series(['ab\n', 'ab\r\n', 'a b', 'Ab', 'Ab', 'AB', ' aBc', 'aBc ', 1, np.nan])
    strings = pd.Series(['ab\n', 'ab\r\n', 'a b', 'Ab', 'Ab', 'AB', ' aBc', 'aBc ', np.nan, np.nan])
    rtype = 'mask_series'

    # pylint: disable=line-too-long
    def test_validation(self):
        results, msg = pdv.validate_string(self.mixed, return_type='values')
        assert_series_equal(results, self.strings)

        _, msg = pdv.validate_string(self.strings, nullable=False, return_type=self.rtype)
        assert ei.nanv in msg

        _, msg = pdv.validate_string(self.strings, unique=True, return_type=self.rtype)
        assert ei.nonu in msg

        _, msg = pdv.validate_string(self.strings, min_length=3, return_type=self.rtype)
        assert ei.strs in msg

        _, msg = pdv.validate_string(self.strings, max_length=2, return_type=self.rtype)
        assert ei.strl in msg

        _, msg = pdv.validate_string(self.strings[:4], case='lower', return_type=self.rtype)
        assert ei.case in msg

        _, msg = pdv.validate_string(self.strings[3:], case='upper', return_type=self.rtype)
        assert ei.case in msg

        _, msg = pdv.validate_string(self.strings[3:], case='title', return_type=self.rtype)
        assert ei.case in msg

        _, msg = pdv.validate_string(self.strings, newlines=False, return_type=self.rtype)
        assert ei.newl in msg

        _, msg = pdv.validate_string(self.strings, whitespace=False, return_type=self.rtype)
        assert ei.whts in msg

        _, msg = pdv.validate_string(self.strings[6:], trailing_whitespace=False, return_type=self.rtype)
        assert ei.whts in msg

        _, msg = pdv.validate_string(self.strings[7:], trailing_whitespace=False, return_type=self.rtype)
        assert ei.whts in msg

        _, msg = pdv.validate_string(self.strings, matching_regex=r'\d', return_type=self.rtype)
        assert ei.remm in msg

        _, msg = pdv.validate_string(self.strings, non_matching_regex=r'[\d\s\w]', return_type=self.rtype)
        assert ei.renm in msg

        _, msg = pdv.validate_string(self.strings, whitelist=self.strings[:4].tolist(), return_type=self.rtype)
        assert ei.whtl in msg

        _, msg = pdv.validate_string(self.strings, blacklist=['a', 'Ab'], return_type=self.rtype)
        assert ei.blkl in msg
