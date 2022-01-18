# Changelog #

The use of this changelog has been deprecated due to the duplicated
effort to keep git and this manual log in sync. As of v0.6.0a1, this
log is no longer in use. Please refer to the git changelog for update
tracking.

## 0.6.0.dev02 ##

Pandas 'match groups' regex warning suppression. README updates.

Match Groups:
- Updated to suppress the pandas warning 'pattern has match groups' which
  is thrown if a regex pattern with match groups is passed into validation.

README:
- Updated README to align with pdvalidate fork.

Released: 2020-06-11


## 0.6.0.dev01 ##

This is a fork from `pandas-validation` and a minor release with the following changes:

* **New functionality:** Updated validation tests to return the error message string along
  with the series mask. This enables the capture and logging of error messages (e.g. for 
  validation reports), which was previously not available.
  **Note:** This will break current integrations of `pandas-validation`.
* Automated testing updated to support new functionality and the removal of ValidationWarning
  warnings from validation tests.
* The function `validate_datetime()` has been removed, per v0.5.0's deprecation notice, and
  replaced by the functions:
  `validate_date()` and `validate_timestamp()`. The new functions validate
  values of types [datetime.date](https://docs.python.org/3/library/datetime.html#datetime.date) and [pandas.Timestamp](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html), respectively.
* Restructured the package for further (future) updates.
* Docstrings updated to Google Style, to fit with S3DEV guidelines.
* Updated reserved words in the code (such as `format`) with non-reserved words.
* Syntax modification for Pythonic-ness, readability and simplicity.
* Addressed a `pandas` `FutureWarning` by converting `datetime` objects using `pd.Timestamp`.
* Added a `_version.py` file to replace hardcoded versioning.  

Released: 2020-06-04


## 0.5.0 ##

This is a minor release with the following changes:

* The function `validate_datetime()` is deprecated and replaced by the functions
  `validate_date()` and `validate_timestamp()`. The new functions validates
  values of types [datetime.date](https://docs.python.org/3/library/datetime.html#datetime.date) and [pandas.Timestamp](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html), respectively.
* Type conversion is no longer carried out by the functions `validate_numeric()`
  and `validate_string()`. It will be up to the user to ensure that the data types
  are correct before the validation.
* Documentation has been updated with two new quickstart examples.

Released: 2019-06-13

[View commits](https://github.com/jmenglund/pandas-validation/compare/v0.4.0...v0.5.0)


## 0.4.0 ##

This is a minor release with the following changes:

* Non-NumPy numeric dtypes should now be supported.
* The ValidationWarning is now issued att stack level 2. This makes it possible to
  trace the line of code that called the function that raised the warning.

Released: 2019-05-27

[View commits](https://github.com/jmenglund/pandas-validation/compare/v0.3.2...v0.4.0)


## 0.3.2 ##

This is a patch release that fixes an issue with validating numbers with `min_value=0`
or `max_value=0`.

Released: 2019-02-02

[View commits](https://github.com/jmenglund/pandas-validation/compare/v0.3.1...v0.3.2)


## 0.3.1 ##

This is a patch release with a few fixes to the documentation.

Released: 2018-10-18

[View commits](https://github.com/jmenglund/pandas-validation/compare/v0.3.0...v0.3.1)


## 0.3.0 ##

This minor release contains the following changes:

* The validation functions now have a `return_type` argument that gives
  the user control over the output. This replaces the `return_values` argument.
* When returning values, the validation functions now filter out all invalid
  values.
* A few tests have been added to `test_pandasvalidation.py`. The test coverage
  is now complete.
* Documentation is up to date.
* Removed use of the deprecated `pandas.tslib`

Released: 2018-01-03

[View commits](https://github.com/jmenglund/pandas-validation/compare/v0.2.0...v0.3.0)


## 0.2.0 ##

This minor release contains the following changes:

* Function `not_convertible()` renamed `mask_nonconvertible()`
* Updated text in `README.rst`
* Updated instructions in `release-checklist.rst`
* Small fixes to the documentation

Released: 2017-09-17

[View commits](https://github.com/jmenglund/pandas-validation/compare/v0.1.1...v0.2.0)


## 0.1.1 ##

This patch release contains a number of small fixes.

* Updated text in `README.rst`
* Updated instructions for Travis-CI (`.travis.yml`)
* Added `release-checklist.rst`
* Libraries for testing removed from `requirements.txt`

Released: 2017-09-15

[View commits](https://github.com/jmenglund/pandas-validation/compare/v0.1.0...v0.1.1)


## 0.1.0 ##

Initial release.

Released: 2016-03-16
