#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for validating data with the library pandas."""

import os
import warnings
import datetime

import numpy
import pandas


__authors__ = "Markus Englund"
__license__ = "MIT"
__version__ = '0.2.0'


class ValidationWarning(Warning):
    pass


def _datetime_to_string(series, format='%Y-%m-%d'):
    """
    Convert datetime values in a pandas Series to strings.
    Other values are left as they are.

    Parameters
    ----------
    series : pandas.Series
        Values to convert.
    format : str
        Format string for datetime type. Default: '%Y-%m-%d'.

    Returns
    -------
    converted : pandas.Series
    """
    converted = series.copy()
    datetime_mask = series.apply(type).isin(
        [datetime.datetime, pandas.tslib.Timestamp])
    if datetime_mask.any():
        converted[datetime_mask] = (
            series[datetime_mask].apply(lambda x: x.strftime(format)))
    return converted.where(datetime_mask, series)


def _numeric_to_string(series, float_format='%g'):
    """
    Convert numeric values in a pandas Series to strings.
    Other values are left as they are.

    Parameters
    ----------
    series : pandas.Series
        Values to convert.
    float_format : str
        Format string for floating point number. Default: '%g'.

    Returns
    -------
    converted : pandas.Series
    """
    converted = series.copy()
    numeric_mask = (
        series.apply(lambda x: numpy.issubdtype(type(x), numpy.number)) &
        series.notnull())
    if numeric_mask.any():
        converted[numeric_mask] = (
            series[numeric_mask].apply(lambda x: float_format % x))
    return converted.where(numeric_mask, series)


def mask_nonconvertible(
        series, to_datatype, datetime_format=None, exact_date=True):
    """
    Return a boolean same-sized object indicating whether values
    cannot be converted.

    Parameters
    ----------
    series : pandas.Series
        Values to check.
    to_datatype : str
        Datatype to which values should be converted. Available values
        are 'numeric' and 'datetime'.
    datetime_format : str
        strftime to parse time, eg '%d/%m/%Y', note that '%f' will parse
        all the way up to nanoseconds. Optional.
    exact_date : bool
        - If True (default), require an exact format match.
        - If False, allow the format to match anywhere in the target string.
    """
    if to_datatype == 'numeric':
        converted = pandas.to_numeric(series, errors='coerce')
    elif to_datatype == 'datetime':
        converted = pandas.to_datetime(
            series, errors='coerce', format=datetime_format, exact=exact_date)
    else:
        raise ValueError(
            'Invalid \'to_datatype\': {}'
            .format(to_datatype))  # pragma: no cover
    notnull = series.copy().notnull()
    mask = notnull & converted.isnull()
    return mask


def to_datetime(
        arg, dayfirst=False, yearfirst=False, utc=None, box=True,
        format=None, exact=True, coerce=None, unit='ns',
        infer_datetime_format=False):
    """
    Convert argument to datetime and set nonconvertible values to NaT.

    This function calls :func:`~pandas.to_datetime` with ``errors='coerce'``
    and issues a warning if values cannot be converted.
    """
    try:
        converted = pandas.to_datetime(
            arg, errors='raise', dayfirst=dayfirst, yearfirst=yearfirst,
            utc=utc, box=box, format=format, exact=exact)
    except:
        converted = pandas.to_datetime(
            arg, errors='coerce', dayfirst=dayfirst, yearfirst=yearfirst,
            utc=utc, box=box, format=format, exact=exact)
        if isinstance(arg, pandas.Series):
            warnings.warn(
                '{}: value(s) not converted to datetime set as NaT'
                .format(repr(arg.name)), ValidationWarning)
        else:  # pragma: no cover
            warnings.warn(
                'Value(s) not converted to datetime set as NaT',
                ValidationWarning)
    return converted


def to_numeric(arg):
    """
    Convert argument to numeric type and set nonconvertible values
    to NaN.

    This function calls :func:`~pandas.to_numeric` with ``errors='coerce'``
    and issues a warning if values cannot be converted.
    """
    try:
        converted = pandas.to_numeric(arg, errors='raise')
    except:
        converted = pandas.to_numeric(arg, errors='coerce')
        if isinstance(arg, pandas.Series):
            warnings.warn(
                '{}: value(s) not converted to numeric set as NaN'
                .format(repr(arg.name)), ValidationWarning)
        else:  # pragma: no cover
            warnings.warn(
                'Value(s) not converted to numeric set as NaN',
                ValidationWarning)
    return converted


def to_string(series, float_format='%g', datetime_format='%Y-%m-%d'):
    """
    Convert values in a pandas Series to strings.

    Parameters
    ----------
    series : pandas.Series
        Values to convert.
    float_format : str
        Format string for floating point number. Default: '%g'.
    datetime_format : str
        Format string for datetime type. Default: '%Y-%m-%d'

    Returns
    -------
    converted : pandas.Series
    """
    converted = _numeric_to_string(series, float_format)
    converted = _datetime_to_string(converted, format=datetime_format)
    converted = converted.astype(str)
    converted = converted.where(series.notnull(), numpy.nan)  # missing as NaN
    return converted


def validate_datetime(
        series, nullable=True, unique=False,
        min_datetime=None, max_datetime=None, return_values=False):
    """
    Validate a pandas Series containing datetimes.

    Parameters
    ----------
    series : pandas.Series
        Values to validate.
    nullable : bool
        If False, check for NaN values. Default: False.
    unique : bool
        If True, check that values are unique. Default: False
    min_datetime : str
        If defined, check for values before min_date. Optional.
    max_datetime : str
        If defined, check for value later than max_date. Optional.
    return_values : bool
        If True, return validated values. Default: False.
    """
    if not series.dtype.type == numpy.datetime64:
        validated = to_datetime(series)
    else:
        validated = series.copy()
    if not nullable and validated.isnull().any():
        warnings.warn(
            '{}: NaT value(s)'
            .format(repr(validated.name)), ValidationWarning)
    if unique and validated.duplicated().any():
        warnings.warn(
            '{}: duplicates'
            .format(repr(validated.name)), ValidationWarning)
    if min_datetime is not None and (validated.dropna() < min_datetime).any():
        warnings.warn(
            '{}: date(s) too early (before {})'
            .format(repr(validated.name), repr(min_datetime)),
            ValidationWarning)
    if max_datetime is not None and (validated.dropna() > max_datetime).any():
        warnings.warn(
            '{}: date(s) too late (after {})'
            .format(repr(validated.name), repr(max_datetime)),
            ValidationWarning)
    if return_values:
        return validated


def validate_numeric(
        series, nullable=True, unique=False, integer=False,
        min_value=None, max_value=None, return_values=False):
    """
    Validate a pandas Series containing numeric values.

    Parameters
    ----------
    series : pandas.Series
        Values to validate.
    nullable : bool
        If False, check for NaN values. Default: True
    unique : bool
        If True, check that values are unique. Default: False
    integer : bool
        If True, check that values are integers. Default: False
    min_value : int
        If defined, check for values below minimum. Optional.
    max_value : int
        If defined, check for value above maximum. Optional.
    return_values : bool
        If True, return validated values. Default: False.
    """
    if not numpy.issubdtype(series.dtype, numpy.number):
        validated = to_numeric(series)
    else:
        validated = series.copy()
    if not nullable and validated.isnull().any():
        warnings.warn(
            '{}: NaN value(s)'
            .format(repr(validated.name)), ValidationWarning)
    if unique and validated.duplicated().any():
        warnings.warn(
            '{}: duplicates'
            .format(repr(validated.name)), ValidationWarning)
    if integer and (validated.dropna() != validated.dropna().apply(int)).any():
        warnings.warn(
            '{}: non-integer(s)'
            .format(repr(validated.name)), ValidationWarning)
    if min_value is not None and (validated.dropna() < min_value).any():
        warnings.warn(
            '{}: value(s) too low (< {})'
            .format(repr(validated.name), min_value), ValidationWarning)
    if max_value is not None and (validated.dropna() > max_value).any():
        warnings.warn(
            '{}: value(s) too high (> {})'
            .format(repr(validated.name), max_value), ValidationWarning)
    if return_values:
        return validated


def validate_string(
        series, nullable=True, unique=False,
        min_length=None, max_length=None, case=None, newlines=True,
        trailing_whitespace=True, whitespace=True, matching_regex=None,
        non_matching_regex=None, whitelist=None, blacklist=None,
        return_values=False):
    """
    Validate a pandas Series with strings. Non-string values
    will be converted to strings prior to validation.

    Parameters
    ----------
    series : pandas.Series
        Values to validate.
    nullable : bool
        If False, check for NaN values. Default: False.
    unique : bool
        If True, check that values are unique. Default: False.
    min_length : int
        If defined, check for strings shorter than
        minimum length. Optional.
    max_length : int
        If defined, check for strings longer than
        maximum length. Optional.
    case : str
        Check for a character case constraint. Available values
        are 'lower', 'upper' and 'title'. Optional.
    newlines : bool
        If False, check for newline characters. Default: True.
    trailing_whitespace : bool
        If False, check for trailing whitespace. Default: True.
    whitespace : bool
         If False, check for whitespace. Default: True.
    matching_regex : str
        Check that strings matches some regular expression. Optional.
    non_matching_regex : str
        Check that strings do not match some regular expression. Optional.
    whitelist : list
        Check that values are in `whitelist`. Optional.
    blacklist : list
        Check that values are not in `blacklist`. Optional.
    return_values : bool
        If True, return validated values. Default: False.
    """
    if series.dropna().apply(lambda x: not isinstance(x, str)).any():
        validated = to_string(series)
    else:
        validated = series.copy()
    if not nullable and validated.isnull().any():
        warnings.warn(
            '{}: NaN value(s)'
            .format(repr(validated.name)), ValidationWarning)
    if unique and validated.duplicated().any():
        warnings.warn(
            '{}: duplicates'.format(repr(validated.name)), ValidationWarning)
    if min_length is not None and (validated.str.len().min() < min_length):
        warnings.warn(
            '{}: string(s) too short (< {} characters)'
            .format(repr(validated.name), min_length), ValidationWarning)
    if max_length is not None and (validated.str.len().max() > max_length):
        warnings.warn(
            '{}: string(s) too long (> {} characters)'
            .format(repr(validated.name), max_length), ValidationWarning)
    if case and not getattr(validated.dropna().str, 'is' + case)().all():
        warnings.warn(
            '{}: wrong case letter(s) (non-{}case)'
            .format(repr(validated.name), case), ValidationWarning)
    if not newlines and validated.str.contains(os.linesep, na=False).any():
        warnings.warn(
            '{}: newline character(s)'
            .format(repr(validated.name)), ValidationWarning)
    if (
        not trailing_whitespace and
        validated.str.contains('^\s|\s$', regex=True, na=False).any()
    ):
        warnings.warn(
            '{}: trailing whitespace'
            .format(repr(validated.name)), ValidationWarning)
    if (
        not whitespace and
        validated.str.contains('\s', regex=True, na=False).any()
    ):
        warnings.warn(
            '{}: whitespace'
            .format(repr(validated.name)), ValidationWarning)
    if matching_regex and not (
        validated.dropna().str.contains(matching_regex, na=True, regex=True)
        .all()
    ):
        warnings.warn(
            '{}: mismatch(es) for "matching regular expression" ({})'
            .format(repr(validated.name), repr(matching_regex)),
            ValidationWarning)
    if non_matching_regex and (
        validated.dropna()
        .str.contains(non_matching_regex, na=False, regex=True)
        .any()
    ):
        warnings.warn(
            '{}: match(es) for "non-matching regular expression" ({})'
            .format(repr(validated.name), repr(non_matching_regex)),
            ValidationWarning)
    if whitelist is not None and not validated.dropna().isin(whitelist).all():
        warnings.warn(
            '{}: Value(s) not in whitelist'
            .format(repr(validated.name)), ValidationWarning)
    if blacklist is not None and validated.dropna().isin(blacklist).any():
        warnings.warn(
            '{}: Value(s) in blacklist'
            .format(repr(validated.name)), ValidationWarning)
    if return_values:
        return validated
