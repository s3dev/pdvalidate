#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides the string-based messages for the test
            suite.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""

from time import sleep


class _Base():
    """General testing messages utility class."""

    @staticmethod
    def _print_testing_start(msg):
        """Print a start of testing message.

        Args:
            msg (str): Short description for this section of tests.

        """
        n = 70
        print('\n\n', '-' * n, sep='')
        print(f'***     Starting test for: {msg}     ***'.center(n))
        print('-' * n, '\n', sep='')
        sleep(0.25)


class _StartOfTest(_Base):
    """Start of test message container class."""

    def startoftest(self, module_name: str):
        """Display the start of test message.

        Args:
            module_name (str): Name of the module being tested.

        """
        self._print_testing_start(msg=module_name)


class _Templates():
    """String templates used across the various unit tests."""

    def __init__(self):
        """Private _Templates class initialiser."""
        self._notexp = self._NotAsExpected()

    @property
    def not_as_expected(self):
        """_NotAsExpected testing templates accessor."""
        return self._notexp


    class _NotAsExpected():
        """'Not as expected' templates for the testing classes."""

        @property
        def general(self):
            """General 'Value not as expected' template."""
            return ('\n\nThe results are not as expected.\n'
                    '- Expected: {}\n'
                    '- Actual: {}')


startoftest = _StartOfTest()
templates = _Templates()
