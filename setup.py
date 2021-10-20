#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:App:       setup.py
:Purpose:   Python library packager.

:Version:   0.2.1
:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@s3dev.uk

:Example:
    Create source and wheel distributions::

        $ cd /path/to/package
        $ python setup.py sdist bdist_wheel

    Simple installation::

        $ cd /path/to/package/dist
        $ pip install <pkgname>-<...>.whl

    git installation::

        $ pip install git+file:///<drive>/path/to/package

    github installation::

        $ pip install git+https://github.com/s3dev/<pkgname>

"""

import os
from setuptools import setup, find_packages
from pdvalidate._version import __version__


class Setup():
    """Create a dist package for this library."""

    PACKAGE         = 'pdvalidate'
    VERSION         = __version__
    PLATFORMS       = 'Python 3.5+'
    DESC            = 'A Python package for validating pandas data structures.'
    AUTHOR          = 'J.M. Englund, J. Berendt'
    AUTHOR_EMAIL    = 'support@s3dev.uk'
    URL             = 'https://github.com/s3dev/pdvalidate'
    LICENSE         = 'MIT'
    KEYWORDS        = ['pandas', 'validation']
    ROOT            = os.path.realpath(os.path.dirname(__file__))
    PACKAGE_ROOT    = os.path.join(ROOT, PACKAGE)
    INCL_PKG_DATA   = False
    CLASSIFIERS     = ['Programming Language :: Python',
                       'Programming Language :: Python :: 3',
                       'Programming Language :: Python :: 3.5',
                       'Programming Language :: Python :: 3.6',
                       'Programming Language :: Python :: 3.7',
                       'Programming Language :: Python :: 3.8',
                       'License :: OSI Approved :: MIT License',
                       'Operating System :: Microsoft :: Windows',
                       'Operating System :: POSIX :: Linux',
                       'Topic :: Software Development',
                       'Topic :: Software Development :: Libraries',
                       'Topic :: Utilities']

    # PACKAGE REQUIREMENTS
    REQUIRES        = ['pandas>=0.22']
    PACKAGES        = find_packages(exclude=['tests*'])

    def run(self):
        """Run the setup."""
        setup(name=self.PACKAGE,
              version=self.VERSION,
              platforms=self.PLATFORMS,
              description=self.DESC,
              author=self.AUTHOR,
              author_email=self.AUTHOR_EMAIL,
              maintainer=self.AUTHOR,
              maintainer_email=self.AUTHOR_EMAIL,
              url=self.URL,
              license=self.LICENSE,
              packages=self.PACKAGES,
              install_requires=self.REQUIRES,
              include_package_data=self.INCL_PKG_DATA,
              classifiers=self.CLASSIFIERS,
              keywords=self.KEYWORDS)

if __name__ == '__main__':
    Setup().run()
