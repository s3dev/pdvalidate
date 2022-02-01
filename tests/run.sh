#!/usr/bin/env bash

printf "\nRunning test cases ...\n"
pytest -v ./test_validation.py
printf "\nDone.\n\n"

#printf "\nRunning doc coverage checks ...\n"
#coverage run -m pytest
#coverage report -m ../pdvalidate/validation.py
#printf "\nDone.\n\n"

