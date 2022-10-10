#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module contains validation rules for ``pandas`` data
            structures.

            In the event of a validation error, the warning is displayed
            to the console and can be returned along with the rows of
            the data structure containing the validation error(s).

:Platform:  Linux/Windows | Python 3.8
:Developer: J Berendt
:Email:     support@s3dev.uk

:Source:    This project (``pdvalidate``) is a fork from Markus Englund's
            ``pandas-validation`` project (v0.5.0), which can be found
            on GitHub:

                ``https://github.com/jmenglund/pandas-validation``

            This fork was built to provide additional functionality,
            specifically the returning of the validation error message
            from the test. Whereas the original project provided a
            ValidationWarning via the ``warnings`` library; which
            prevented the validation error from being logged.

            We have worked to keep the initial integrity of the project,
            while adding some features. Additionally, the automated
            testing suite (via ``pytest``) has also been maintained.

            Thank you Markus for the excellent framework, and for
            sharing it with us all!

:Example Use:

            Example code use::

                >>> import pandas as pd
                >>> from pdvalidate.validation import validate as pdv

                >>> s = pd.Series(['aaa', 'bb', 'c'], name='TestSeries')
                >>> result, msg = pdv.validate_string(s,
                                                      min_length=1,
                                                      max_length=2,
                                                      return_type='mask_series')

                [RangeWarning]: 'TestSeries': string(s) too long.

                # Show row(s) which fail validation.
                >>> print(s[result])

                0    aaa
                Name: TestSeries, dtype: object

"""
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches

import datetime
import os
import warnings
import numpy as np
import pandas as pd
from utils4.user_interface import ui


class ErrorInfo():
    """Define the dictionary lookups for error descriptions."""

    blkl = 'string(s) in blacklist'
    case = 'wrong case letter(s)'
    elyd = 'date(s) too early'
    elyt = 'timestamp(s) too early'
    hghv = 'value(s) too high'
    lowv = 'value(s) too low'
    lted = 'date(s) too late'
    ltet = 'timestamp(s) too late'
    nann = 'Non-numeric value(s) set as NaN'
    nans = 'Non-string value(s) set as NaN'
    nanv = 'NaN value(s)'
    natd = 'Value(s) not of type datetime.date set as NaT'
    natt = 'Value(s) not of type pandas.Timestamp set as NaT'
    natv = 'NaT value(s)'
    newl = 'newline character(s)'
    nint = 'non-integer(s)'
    nonu = 'duplicates'
    remm = 'mismatch(es) for "matching regular expression"'
    renm = 'match(es) for "non-matching regular expression"'
    strl = 'string(s) too long'
    strs = 'string(s) too short'
    whtl = 'string(s) not in whitelist'
    whts = 'whitespace'
    whtt = 'trailing whitespace'

    @property
    def validate_date(self) -> dict:
        """Date validation error descriptors."""
        info = {'invalid_type': self.natd,
                'isnull': self.natv,
                'nonunique': self.nonu,
                'too_early': self.elyd,
                'too_late': self.lted}
        return info

    @property
    def validate_numeric(self) -> dict:
        """Numeric validation error descriptors."""
        info = {'invalid_type': self.nann,
                'isnull': self.nanv,
                'nonunique': self.nonu,
                'noninteger': self.nint,
                'too_low': self.lowv,
                'too_high': self.hghv}
        return info

    @property
    def validate_string(self) -> dict:
        """String validation error descriptors."""
        info = {'invalid_type': self.nans,
                'isnull': self.nanv,
                'nonunique': self.nonu,
                'too_short': self.strs,
                'too_long': self.strl,
                'wrong_case': self.case,
                'newlines': self.newl,
                'trailing_space': self.whtt,
                'whitespace': self.whts,
                'regex_mismatch': self.remm,
                'regex_match': self.renm,
                'not_in_whitelist': self.whtl,
                'in_blacklist': self.blkl}
        return info

    @property
    def validate_timestamp(self) -> dict:
        """Timestamp validation error descriptors."""
        info = {'invalid_type': self.natt,
                'isnull': self.natv,
                'nonunique': self.nonu,
                'too_early': self.elyt,
                'too_late': self.ltet}
        return info


class ValidationWarning(Warning):
    """Define the project's ValidationWarning class."""


class Validation():
    """Class container for all validation functionality."""

    ei = ErrorInfo()

    @staticmethod
    def mask_nonconvertible(series,
                            to_datatype,
                            datetime_format=None,
                            exact_date=True) -> pd.Series:
        """Determine if values cannot be converted.

        Args:
            series (pd.Series): Values to check.
            to_datatype (str): Datatype to which values should be converted.
                Available options are 'numeric' and 'datetime'.
            datetime_format (str): Format code. (e.g. '%d/%m/%Y')
                Note that '%f' will parse nanoseconds to six decimal places.
                Optional.
            exact_date (bool):
                - If True (default), require an exact format match.
                - If False, allow the format to match anywhere in the
                  target string.

        Returns:
            A boolean same-sized object indicating whether values cannot
            be converted.

        """
        if to_datatype == 'numeric':
            converted = pd.to_numeric(series,
                                      errors='coerce')
        elif to_datatype == 'datetime':
            converted = pd.to_datetime(series,
                                       errors='coerce',
                                       format=datetime_format,
                                       exact=exact_date)
        else:
            raise ValueError(f'Invalid \'to_datatype\': {to_datatype}')  # pragma: no cover
        notnull = series.copy().notnull()
        mask = notnull & converted.isnull()
        return mask

    @staticmethod
    def test_dtype_numeric(series: pd.Series) -> bool:
        """Test if the Series has a numeric datatype.

        Args:
            series (pd.Series): Series to be tested.

        Returns:
            bool: True if a numeric datatype, otherwise False.

        """
        return pd.api.types.is_numeric_dtype(series.dtype)

    @staticmethod
    def test_dtype_object(series: pd.Series) -> bool:
        """Test if the Series has an object datatype.

        Args:
            series (pd.Series): Series to be tested.

        Returns:
            bool: True if an object datatype, otherwise False.

        """
        return pd.api.types.is_object_dtype(series.dtype)

    @staticmethod
    def to_datetime(arg,
                    dayfirst=False,
                    yearfirst=False,
                    utc=None,
                    datetime_format=None,
                    exact=True) -> pd.Series:
        """Convert argument to datetime. Set nonconvertible values to NaT.

        This function calls :func:`~pd.to_datetime` with ``errors='coerce'``
        and issues a warning if values cannot be converted.

        Args:
            arg (Union[int, float, str, datetime, list, tuple, pd.Series, pd.DataFrame, dict]):
                Values to convert.

        For help on other arguments, run: ``help(pandas.to_datetime)``.

        Returns:
            pd.Series: A converted pd.Series.

        """
        try:
            converted = pd.to_datetime(arg,
                                       errors='raise',
                                       dayfirst=dayfirst,
                                       yearfirst=yearfirst,
                                       utc=utc,
                                       format=datetime_format,
                                       exact=exact)
        except ValueError:
            converted = pd.to_datetime(arg,
                                       errors='coerce',
                                       dayfirst=dayfirst,
                                       yearfirst=yearfirst,
                                       utc=utc,
                                       format=datetime_format,
                                       exact=exact)
            if isinstance(arg, pd.Series):
                msg = '{}: value(s) not converted to datetime set as NaT'
                msg = msg.format(repr(arg.name))
                warnings.warn(msg, ValidationWarning, stacklevel=2)
            else:  # pragma: no cover
                msg = 'Value(s) not converted to datetime set as NaT'
                warnings.warn(msg, ValidationWarning, stacklevel=2)
        return converted

    @staticmethod
    def to_numeric(arg) -> pd.Series:
        """Convert argument to numeric type. Set nonconvertible values to NaN.

        This function calls :func:`~pd.to_numeric` with ``errors='coerce'``
        and issues a warning if values cannot be converted.

        Args:
            arg (list, tuple, 1-d array, or Series): Values to convert.

        For help on other arguments, run: ``help(pandas.to_numeric)``.

        Returns:
            A converted pd.Series.

        """
        try:
            converted = pd.to_numeric(arg, errors='raise')
        except ValueError:
            converted = pd.to_numeric(arg, errors='coerce')
            if isinstance(arg, pd.Series):
                msg = '{}: value(s) not converted to numeric set as NaN'
                msg = msg.format(repr(arg.name))
                warnings.warn(msg, ValidationWarning, stacklevel=2)
            else:  # pragma: no cover
                msg = 'Value(s) not converted to numeric set as NaN'
                warnings.warn(msg, ValidationWarning, stacklevel=2)
        return converted

    def to_string(self,
                  series,
                  float_format='%g',
                  datetime_format='%Y-%m-%d') -> pd.Series:
        """Convert values in a pandas Series to strings.

        Args:
            series (pd.Series): Values to convert.
        float_format (str): Format code for floating point number.
            Default: '%g'.
        datetime_format (str): Format code for datetime type.
            Default: '%Y-%m-%d'.

        Returns:
            A converted pd.Series.

        """
        converted = self._numeric_to_string(series, float_format)
        converted = self._datetime_to_string(converted, datetime_format=datetime_format)
        converted = converted.astype(str)
        converted = converted.where(series.notnull(), np.nan)  # missing as NaN
        return converted

    def validate_date(self,
                      series,
                      convert=False,
                      dateformat=None,
                      nullable=True,
                      unique=False,
                      min_date=None,
                      max_date=None,
                      return_type=None):
        """Validate a pandas Series with values of type ``datetime.date``.

        Values of a different data type will be replaced with NaN prior to
        the validation.

        Args:
            series (pd.Series): Values to validate.
            convert (bool, optional): Convert the Series to datetime using the
                :func:`~pd.to_datetime` function. Also use the ``dateformat``
                parameter to define the format. Defaults to False.
            dateformat (str, optional): Format code for the datetimes being
                passed in the Series. For use with the ``convert`` parameter.
                Defaults to None.
            nullable (bool, optional): If False, check for NaN values.
                Defaults to True.
            unique (bool, optional): If True, check that values are unique.
                Defaults to False
            min_date (datetime.date, optional): If defined, check for values
                before ``min_date``, inclusive. Defaults to None.
            max_date (datetime.date, optional): If defined, check for value
                later than ``max_date``, inclusive. Defaults to None.
            return_type (str, optional): Kind of data object to return.
                Options: 'mask_series', 'mask_frame', 'values'.
                Defaults to None.

        Returns:
            tuple: If a ``return_type`` is specified, a tuple of::

                (return_object, error_messages)

        """
        masks = {}
        results = None
        if all([convert, dateformat]):
            series = pd.to_datetime(series, format=dateformat)  # pragma: no cover
        is_date = series.apply(lambda x: isinstance(x, datetime.date))
        masks['invalid_type'] = ~is_date & series.notnull()
        to_validate = series.where(is_date)
        if not nullable:
            masks['isnull'] = to_validate.isnull()
        if unique:
            masks['nonunique'] = to_validate.duplicated() & to_validate.notnull()
        if min_date:
            masks['too_early'] = to_validate.dropna() < pd.Timestamp(min_date)
        if max_date:
            masks['too_late'] = to_validate.dropna() > pd.Timestamp(max_date)
        msg_list = self._get_error_messages(masks, self.ei.validate_date)
        msg = self._build_message_range(series_name=repr(series.name), message_list=msg_list)
        if return_type:
            results = (self._get_return_object(masks, to_validate, return_type), msg)
        return results

    def validate_timestamp(self,
                           series,
                           nullable=True,
                           unique=False,
                           min_timestamp=None,
                           max_timestamp=None,
                           return_type=None):
        """Validate a pandas Series with values of type `pandas.Timestamp`.

        Values of a different data type will be replaced with NaT prior to
        the validation.

        Args:
            series (pd.Series): Values to validate.
            nullable (bool, optional): If False, check for NaN values.
                Defaults to True.
            unique (bool, optional): If True, check that values are unique.
                Defaults to False.
            min_timestamp (pd.Timestamp, optional): If defined, check for
                values before ``min_timestamp``, inclusive. Defaults to None.
            max_timestamp (pd.Timestamp, optional): If defined, check for
                value later than ``max_timestamp``, inclusive.
                Defaults to None.
            return_type (str, optional): Kind of data object to return.
                Options: 'mask_series', 'mask_frame', 'values'.
                Defaults to None.

        Returns:
            tuple: If a ``return_type`` is specified, a tuple of::

                (return_object, error_messages)

        """
        masks = {}
        results = None
        is_timestamp = series.apply(lambda x: isinstance(x, pd.Timestamp))
        masks['invalid_type'] = ~is_timestamp & series.notnull()
        to_validate = pd.to_datetime(series.where(is_timestamp, pd.NaT))
        if not nullable:
            masks['isnull'] = to_validate.isnull()
        if unique:
            masks['nonunique'] = to_validate.duplicated() & to_validate.notnull()
        if min_timestamp:
            masks['too_early'] = to_validate.dropna() < min_timestamp
        if max_timestamp:
            masks['too_late'] = to_validate.dropna() > max_timestamp
        msg_list = self._get_error_messages(masks, self.ei.validate_timestamp)
        msg = self._build_message_range(series_name=repr(series.name), message_list=msg_list)
        if return_type:
            results = (self._get_return_object(masks, to_validate, return_type), msg)
        return results

    def validate_numeric(self,
                         series,
                         nullable=True,
                         unique=False,
                         integer=False,
                         min_value=None,
                         max_value=None,
                         return_type=None):
        """Validate a pandas Series containing numeric values.

        Args:
            series (pd.Series): Values to validate.
            nullable (bool, optional): If False, check for NaN values.
                Defaults to True.
            unique (bool, optional): If True, check that values are unique.
                Defaults to False.
            integer (bool, optional): If True, check that values are integers.
                Defaults to False.
            min_value (int, optional): If defined, check for values below
                minimum, inclusive. Defaults to None.
            max_value (int, optional): If defined, check for value above
                maximum, inclusive. Defaults to None.
            return_type (str, optional): Kind of data object to return.
                Options: 'mask_series', 'mask_frame', 'values'.
                Defaults to None.

        Returns:
            tuple: If a ``return_type`` is specified, a tuple of::

                (return_object, error_messages)

        """
        results = None
        masks = {}
        is_numeric = series.apply(pd.api.types.is_number)
        masks['invalid_type'] = ~is_numeric & series.notnull()
        to_validate = pd.to_numeric(series.where(is_numeric))
        # Only carry out tests if dtype is numeric.
        if self.test_dtype_numeric(series=series):
            if not nullable:
                masks['isnull'] = to_validate.isnull()
            if unique:
                masks['nonunique'] = to_validate.duplicated() & to_validate.notnull()
            if integer:
                noninteger_dropped = (to_validate.dropna() != to_validate.dropna().apply(int))
                masks['noninteger'] = pd.Series(noninteger_dropped, series.index)
            if min_value is not None:
                masks['too_low'] = to_validate.dropna() < min_value
            if max_value is not None:
                masks['too_high'] = to_validate.dropna() > max_value
            msg_list = self._get_error_messages(masks, self.ei.validate_numeric)
            msg = self._build_message_range(series_name=repr(series.name), message_list=msg_list)
        else:
            msg = self._build_message_dtype(series_name=repr(series.name),
                                            exp='numeric',
                                            rec=series.dtype)
        if return_type:
            results = (self._get_return_object(masks, to_validate, return_type), msg)
        return results

    def validate_string(self,
                        series,
                        nullable=True,
                        unique=False,
                        min_length=None,
                        max_length=None,
                        case=None,
                        newlines=True,
                        trailing_whitespace=True,
                        whitespace=True,
                        matching_regex=None,
                        non_matching_regex=None,
                        whitelist=None,
                        blacklist=None,
                        return_type=None):
        r"""Validate a pandas Series with strings.

        Non-string values will be flagged as errors.

        Args:
            series (pd.Series): Values to validate.
            nullable (bool, optional): If False, check for NaN values.
                Defaults to True.
            unique (bool, optional): If True, check that values are unique.
                Defaults to False.
            min_length (int, optional): If defined, check for strings shorter
                than ``min_length``, inclusive. Defaults to None.
            max_length (int, optional): If defined, check for strings longer
                than ``max_length``, inclusive. Defaults to None.
            case (str, optional): Check for a character case constraint.
                Options: 'lower', 'upper', 'title'. Defaults to None.
            newlines (bool, optional): If False, check for platform-specific
                newline characters.
                Note: Linux searches for '\n'. Windows searches for '\r\n'
                Defaults to True.
            trailing_whitespace (bool, optional): If False, check for trailing
                whitespace. Defaults to True.
            whitespace (bool, optional): If False, check for whitespace.
                Defaults to True.
            matching_regex (str, optional): Check that strings match the
                provided regular expression. Defaults to None.
            non_matching_regex (str, optional): Check that strings do not
                match the provided regular expression. Defaults to None.
            whitelist (list, optional): Check that values are in ``whitelist``.
                Defaults to None.
            blacklist (list, optional): Check that values are not in
                ``blacklist``. Defaults to None.
            return_type (str, optional): Kind of data object to return.
                Options: 'mask_series', 'mask_frame', 'values'. Defaults to
                None.

        Returns:
            tuple: If a ``return_type`` is specified, a tuple of::

                (return_object, error_messages)

        """
        results = None
        masks = {}
        is_string = series.apply(lambda x: isinstance(x, str))
        masks['invalid_type'] = ~is_string & series.notnull()
        to_validate = series.where(is_string)
        # Only carry out tests if dtype is object.
        if self.test_dtype_object(series=series):
            if not nullable:
                masks['isnull'] = to_validate.isnull()
            if unique:
                masks['nonunique'] = to_validate.duplicated() & to_validate.notnull()
            if min_length is not None:
                too_short_dropped = to_validate.dropna().apply(len) < min_length
                masks['too_short'] = pd.Series(too_short_dropped, series.index)
            if max_length is not None:
                too_long_dropped = to_validate.dropna().apply(len) > max_length
                masks['too_long'] = pd.Series(too_long_dropped, series.index)
            if whitelist:
                masks['not_in_whitelist'] = (to_validate.notnull() & ~to_validate.isin(whitelist))
            if blacklist:
                masks['in_blacklist'] = to_validate.isin(blacklist)
            # Test Series contains string values.
            # The .str accessor will fall over if string values are not present.
            if (~to_validate.isnull()).any():
                if case:
                    altered_case = getattr(to_validate.str, case)()
                    wrong_case_dropped = (altered_case.dropna() !=
                                          to_validate[altered_case.notnull()])
                    masks['wrong_case'] = pd.Series(wrong_case_dropped, series.index)
                if not newlines:
                    masks['newlines'] = to_validate.str.contains(os.linesep)
                if trailing_whitespace is False:
                    masks['trailing_space'] = to_validate.str.contains(r'^\s|\s$', regex=True)
                if not whitespace:
                    masks['whitespace'] = to_validate.str.contains(r'\s', regex=True)
                if matching_regex:
                    # Ignore warning for regex patterns with unused matching groups
                    warnings.filterwarnings('ignore', 'This pattern has match groups.')
                    masks['regex_mismatch'] = (to_validate.str.contains(matching_regex, regex=True)
                                               .apply(lambda x: x is False) & to_validate.notnull())
                if non_matching_regex:
                    # Ignore warning for regex patterns with unused matching groups
                    warnings.filterwarnings('ignore', 'This pattern has match groups.')
                    masks['regex_match'] = to_validate.str.contains(non_matching_regex, regex=True)
            msg_list = self._get_error_messages(masks, self.ei.validate_string)
            msg = self._build_message_range(series_name=repr(series.name), message_list=msg_list)
        else:
            msg = self._build_message_dtype(series_name=series.name,
                                            exp='object',
                                            rec=series.dtype)
        if return_type:
            results = (self._get_return_object(masks, to_validate, return_type), msg)
        return results

    @staticmethod
    def _build_message_range(series_name: str, message_list: list) -> str:
        """Build the range warning message string for terminal output.

        Args:
            series_name (str): Name of the Series causing the error.
            message_list (list): List of error message strings to be printed to
                the terminal.

        Returns:
            str: Compiled error message string.

        """
        msg = ''
        if message_list:
            msg = f'[RangeWarning]: {series_name}: {"; ".join(message_list)}.'
            ui.print_warning(msg)
        return msg

    @staticmethod
    def _build_message_dtype(series_name: str, exp: str, rec: str) -> str:
        """Build the unexpected datatype warning message for terminal output.

        Args:
            series_name (str): Name of the Series causing the error.
            exp (str): Expected datatype.
            rec (str): Received datatype.

        Returns:
            str: Compiled error message string.

        """
        msg = (f'[DatatypeWarning]: {series_name}: Expected {exp}, received {rec}. '
                'Please address and re-validate.')
        ui.print_warning(msg)
        return msg

    @staticmethod
    def _datetime_to_string(series, datetime_format='%Y-%m-%d') -> pd.Series:
        """Convert datetime values in a pandas Series to strings.

        Other values are left as they are.

        Args:
            series (pd.Series): Values to convert.
            datetime_format (str): Format code for datetime type.
                Default: '%Y-%m-%d'.

        Returns:
            A converted pd.Series.

        """
        converted = series.copy(deep=True)
        datetime_mask = series.apply(type).isin([datetime.datetime, pd.Timestamp])
        if datetime_mask.any():
            converted[datetime_mask] = (series[datetime_mask]
                                        .apply(lambda x: x.strftime(datetime_format)))
        return converted.where(datetime_mask, series)

    @staticmethod
    def _get_error_messages(masks, error_info) -> list:
        """Compile a list of error messages.

        Args:
            masks (list) List of pd.Series with masked errors.
            error_info (dict): Dictionary with error messages corresponding
                to different validation errors.

        Returns:
            A compiled list of error messages.

        """
        return [error_info[k] for k, v in masks.items() if v.any()]

    @staticmethod
    def _get_return_object(masks: dict, values: pd.Series, return_type: str) -> pd.Series:
        """Build the return object.

        Args:
            masks (dict): Dictionary of validation failure masks.
            values (pd.Series): Series of values which were validated.
            return_type (str): Return type string descriptor.

        Raises:
            ValueError: For an invalid return type string.

        Returns:
            pd.Series: Series containing the records which failed validation.

        """
        mask_frame = pd.concat(masks, axis='columns')
        ro = None
        if return_type == 'mask_frame':
            ro = mask_frame
        elif return_type == 'mask_series':
            ro = mask_frame.any(axis=1)
        elif return_type == 'values':
            ro = values.where(~mask_frame.any(axis=1))
        else:
            raise ValueError('Invalid return_type')
        return ro

    @staticmethod
    def _numeric_to_string(series, float_format='%g') -> pd.Series:
        """Convert numeric values in a pandas Series to strings.

        Other values are left as they are.

        Args:
            series (pd.Series): Values to convert.
            float_format (str): Format code for floating point number.
                Default: '%g'.

        Returns:
            A converted pd.Series.

        """
        converted = series.copy(deep=True)
        numeric_mask = (series.apply(lambda x: np.issubdtype(type(x), np.number)) &
                        series.notnull())
        if numeric_mask.any():
            converted[numeric_mask] = (series[numeric_mask]
                                       .apply(lambda x: float_format % x))
        return converted.where(numeric_mask, series)


ei  = ErrorInfo()
validate = Validation()
