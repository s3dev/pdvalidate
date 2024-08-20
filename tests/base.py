#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides the superclass which is to be inherited
            by the test-specific modules.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Example:
    Example code use.

    Run all tests via the shell script::

        $ ./run.sh

    Run all tests using unittest::

        $ python -m unittest discover

    Run a single test::

        $ python -m unittest test_name.py

"""
# pylint: disable=wrong-import-position

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# Set sys.path for relative imports ^^^
import io
import unittest


class TestBase(unittest.TestCase):
    """Private generalised base-testing class.

    This class is designed to be inherited by each test-specific class.

    """
    # Allow room for the side comments.
    # pylint: disable=line-too-long

    _DIR_ROOT = os.path.realpath(os.path.dirname(__file__))
    _DIR_RESC = os.path.join(_DIR_ROOT, 'resources')                # Path to the test resources directory.
    _DIR_VER_DATA = os.path.join(_DIR_RESC, 'data')                 # Path to the verification data directory.

    @classmethod
    def setUpClass(cls):
        """Run this method at the start of all tests in this module.

        :Tasks:

            - Ignore the listed warnings.

        """

    @classmethod
    def tearDownClass(cls):
        """Teardown the testing class once all tests are complete."""

    @staticmethod
    def strip_ansi_colour(text: str) -> iter:
        """Strip ANSI colour sequences from a string.

        Args:
            text (str): Text string to be stripped.

        Returns:
            Iterator[str]: A generator for each returned character. Note,
            this will include newline characters.

        """
        # pylint: disable=multiple-statements
        buff = io.StringIO(text)
        while (b := buff.read(1)):
            if b == '\x1b':
                while ( b := buff.read(1) ) != 'm': continue
            else:
                yield b
