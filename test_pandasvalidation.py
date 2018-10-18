#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import warnings

import pytest
import numpy
import pandas

from pandas.util.testing import assert_series_equal, assert_frame_equal

from pandasvalidation import (
    ValidationWarning,
    _datetime_to_string,
    _numeric_to_string,
    _get_return_object,
    mask_nonconvertible,
    to_datetime,
    to_numeric,
    to_string,
    validate_datetime,
    validate_numeric,
    validate_string)


class TestReturnTypes():

    strings = pandas.Series(['1', '1', 'ab\n', 'a b', 'Ab', 'AB', numpy.nan])
    masks = [
        pandas.Series([False, False, False, True, True, False, False]),
        pandas.Series([True, True, False, True, True, False, True])]

    def test_return_mask_series(self):
        assert_series_equal(
            _get_return_object(self.masks, self.strings, 'mask_series'),
            pandas.Series([True, True, False, True, True, False, True]))

    def test_return_mask_frame(self):
        assert_frame_equal(
            _get_return_object(self.masks, self.strings, 'mask_frame'),
            pandas.concat(self.masks, axis='columns'))

    def test_return_values(self):
        assert_series_equal(
            _get_return_object(self.masks, self.strings, 'values'),
            pandas.Series([
                numpy.nan, numpy.nan, 'ab\n', numpy.nan,
                numpy.nan, 'AB', numpy.nan]))

    def test_wrong_return_type(self):
        with pytest.raises(ValueError):
            _get_return_object(self.masks, self.strings, 'wrong return type')


class TestMaskNonconvertible():

    mixed = pandas.Series([
        1, 2.3, numpy.nan, 'abc', pandas.datetime(2014, 1, 7), '2014'])

    inconvertible_numeric = pandas.Series(
        [False, False, False, True, True, False])

    inconvertible_exact_dates = pandas.Series(
        [True, True, False, True, True, False])

    inconvertible_inexact_dates = pandas.Series(
        [True, True, False, True, False, False])

    def test_numeric(self):
        assert_series_equal(
            mask_nonconvertible(self.mixed, 'numeric'),
            self.inconvertible_numeric)

    def test_datetime_exact_date(self):
        assert_series_equal(
            mask_nonconvertible(
                self.mixed, 'datetime', datetime_format='%Y', exact_date=True),
            self.inconvertible_exact_dates)

        assert_series_equal(
            mask_nonconvertible(
                self.mixed, 'datetime', datetime_format='%Y',
                exact_date=False), self.inconvertible_inexact_dates)


class TestToDatetime():

    mixed = pandas.Series([
        1, 2.3, numpy.nan,
        'abc', pandas.datetime(2014, 1, 7), '2014'])

    def test_exact(self):
        assert (
            to_datetime(self.mixed, format='%Y', exact=True).tolist() == [
                pandas.NaT, pandas.NaT, pandas.NaT, pandas.NaT,
                pandas.NaT, pandas.Timestamp('2014-01-01 00:00:00')])
        assert (
            to_datetime(self.mixed, format='%Y', exact=False).tolist() == [
                pandas.NaT, pandas.NaT, pandas.NaT, pandas.NaT,
                pandas.Timestamp('2014-01-01 00:00:00'),
                pandas.Timestamp('2014-01-01 00:00:00')])


class TestToNumeric():

    mixed = pandas.Series([
        1, 2.3, numpy.nan, 'abc', pandas.datetime(2014, 1, 7), '2014'])

    def test_conversion(self):
        assert (
            to_numeric(self.mixed).sum() == 2017.3)

        pytest.warns(ValidationWarning, to_numeric, self.mixed)


class TestToString():

    mixed = pandas.Series(
        [1, 2.3, numpy.nan, 'abc', pandas.datetime(2014, 1, 7)])

    numeric_as_strings = pandas.Series(
        ['1', '2.3', numpy.nan, 'abc', pandas.datetime(2014, 1, 7)])

    datetimes_as_strings = pandas.Series(
        [1, 2.3, numpy.nan, 'abc', '2014-01-07'])

    all_values_as_strings = pandas.Series(
        ['1', '2.3', numpy.nan, 'abc', '2014-01-07'])

    def test_numeric_to_string(self):
        assert_series_equal(
            _numeric_to_string(self.mixed), self.numeric_as_strings)

    def test_datetime_to_string(self):
        assert_series_equal(
            _datetime_to_string(self.mixed, format='%Y-%m-%d'),
            self.datetimes_as_strings)

    def test_to_string(self):
        assert_series_equal(
            to_string(
                self.mixed, float_format='%g', datetime_format='%Y-%m-%d'),
            self.all_values_as_strings)


class TestValidateDatetime():

    dates_as_strings = pandas.Series([
        '2014-01-07', '2014-01-07', '2014-02-28', numpy.nan])

    dates = pandas.Series([
        datetime.datetime(2014, 1, 7), datetime.datetime(2014, 1, 7),
        datetime.datetime(2014, 2, 28), numpy.nan])

    def test_validation(self):

        assert_series_equal(
            validate_datetime(self.dates_as_strings, return_type='values'),
            validate_datetime(self.dates, return_type='values'))

        pytest.warns(
            ValidationWarning, validate_datetime, self.dates, nullable=False)

        pytest.warns(
            ValidationWarning, validate_datetime, self.dates, unique=True)

        pytest.warns(
            ValidationWarning, validate_datetime, self.dates,
            min_datetime='2014-01-08')

        pytest.warns(
            ValidationWarning, validate_datetime, self.dates,
            max_datetime='2014-01-08')


class TestValidateNumber():

    numeric_as_strings = pandas.Series(['1', '1', '2.3', numpy.nan])
    numeric = pandas.Series([1, 1, 2.3, numpy.nan])

    def test_validation(self):

        assert_series_equal(
            validate_numeric(self.numeric_as_strings, return_type='values'),
            validate_numeric(self.numeric, return_type='values'))

        pytest.warns(
            ValidationWarning, validate_numeric, self.numeric, nullable=False)

        pytest.warns(
            ValidationWarning, validate_numeric, self.numeric, unique=True)

        pytest.warns(
            ValidationWarning, validate_numeric, self.numeric, integer=True)

        pytest.warns(
            ValidationWarning, validate_numeric, self.numeric, min_value=2)

        pytest.warns(
            ValidationWarning, validate_numeric, self.numeric, max_value=2)


class TestValidateString():

    mixed = pandas.Series([1, 1, 'ab\n', 'a b', 'Ab', 'AB', numpy.nan])
    strings = pandas.Series(['1', '1', 'ab\n', 'a b', 'Ab', 'AB', numpy.nan])

    def test_validation(self):

        assert_series_equal(
            validate_string(self.mixed, return_type='values'),
            validate_string(self.strings, return_type='values'))

        pytest.warns(
            ValidationWarning, validate_string, self.strings, nullable=False)

        pytest.warns(
            ValidationWarning, validate_string, self.strings, unique=True)

        pytest.warns(
            ValidationWarning, validate_string, self.strings, min_length=2)

        pytest.warns(
            ValidationWarning, validate_string, self.strings, max_length=2)

        pytest.warns(
            ValidationWarning, validate_string, self.strings[3:], case='lower')

        pytest.warns(
            ValidationWarning, validate_string, self.strings[3:], case='upper')

        pytest.warns(
            ValidationWarning, validate_string, self.strings[3:], case='title')

        pytest.warns(
            ValidationWarning, validate_string, self.strings, newlines=False)

        pytest.warns(
            ValidationWarning, validate_string, self.strings,
            trailing_whitespace=False)

        pytest.warns(
            ValidationWarning, validate_string, self.strings, whitespace=False)

        pytest.warns(
            ValidationWarning, validate_string, self.strings,
            matching_regex=br'\d')

        pytest.warns(
            ValidationWarning, validate_string, self.strings,
            non_matching_regex=br'[\d\s\w]')

        pytest.warns(
            ValidationWarning, validate_string, self.strings,
            whitelist=self.strings[:5])

        pytest.warns(
            ValidationWarning, validate_string, self.strings,
            blacklist=['a', 'Ab'])
