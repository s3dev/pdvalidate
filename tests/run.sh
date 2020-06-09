#!/usr/bin/env bash

printf "\nRunning source code test ...\n\n"
pytest -v ./test_validation.py


printf "\nRunning test coverage tests ...\n\n"
coverage run -m pytest test_validation.py
coverage report -m ../pdvalidate/validation.py


printf "\nAll tests complete.\n\n"
