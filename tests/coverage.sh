#!/usr/bin/bash

printf "\nSetting up ...\n"
coverage run -m pytest

printf "\n\nRunning coverage test(s) ...\n"
coverage report -m ../pdvalidate/validation.py
coverage html

printf "\n\n"
