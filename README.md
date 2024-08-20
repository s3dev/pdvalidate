# A simple library for validating pandas data structures

[![PyPI - Version](https://img.shields.io/pypi/v/pdvalidate?style=flat-square)](https://pypi.org/project/pdvalidate)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/pdvalidate?style=flat-square)](https://pypi.org/project/pdvalidate)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pdvalidate?style=flat-square)](https://pypi.org/project/pdvalidate)
[![PyPI - Status](https://img.shields.io/pypi/status/pdvalidate?style=flat-square)](https://pypi.org/project/pdvalidate)
[![Static Badge](https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square)](https://pypi.org/project/pdvalidate)
[![Static Badge](https://img.shields.io/badge/code_coverage-100%25-brightgreen?style=flat-square)](https://pypi.org/project/pdvalidate)
[![Static Badge](https://img.shields.io/badge/pylint_analysis-100%25-brightgreen?style=flat-square)](https://pypi.org/project/pdvalidate)
[![Documentation Status](https://readthedocs.org/projects/pdvalidate/badge/?version=latest&style=flat-square)](https://pdvalidate.readthedocs.io/en/latest/)
[![PyPI - License](https://img.shields.io/pypi/l/virtualenv?style=flat-square)](https://opensource.org/licenses/MIT)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/pdvalidate?style=flat-square)](https://pypi.org/project/pdvalidate)

This ``pdvalidate`` library is a fork from ``pandas-validation`` (v0.5.0) originally written by Markus Englund, and was enhanced to include additional functionality; specifically to return the validation error messages (from each test) to the caller for capture and logging purposes.

Great efforts have been made to retain the initial integrity of the original ``pandas-validation`` project, while adding some new features.

Thank you Markus for your hard work on the excellent framework, and for sharing it with us all.


## Installation

For most users, the easiest way is probably to install the latest version hosted on [PyPI](https://pypi.org/project/pdvalidate/), *after* activating the appropriate virtual environment.

    pip install pdvalidate


## Using the Library
The [Quickstart Guide](https://pdvalidate.readthedocs.io/en/latest/quickstart.html) section of the documentation can be used to get up and running. Whereas, the [documentation suite](https://pdvalidate.readthedocs.io/en/latest/index.html) contains usage examples and detailed explanation for each of the library's importable modules.


## License

`pdvalidate` is distributed under the [MIT License](https://opensource.org/licenses/MIT).


## Authors
- Markus Englund: Author of the *original* [`pandas-validation`](https://github.com/jmenglund/pandas-validation).
- The S3DEV Developers: Authors of *this* [`pdvalidate`](https://github.com/s3dev/pdvalidate) fork, for enhanced functionality.
