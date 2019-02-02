# Changelog #

Tracking changes in pandas-validation between versions.
See also https://github.com/jmenglund/pandas-validation/releases.


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
