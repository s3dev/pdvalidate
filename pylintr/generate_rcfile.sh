#!/usr/bin/env bash 

disables=''
disable=(
    "fixme"
    "broad-except"
)

# Build string of items to disable.
for i in ${disable[@]}; do disables+="${i},"; done

# Generate a custom, project-specific config file.
pylint --reports=yes --disable="${disables}" --generate-rcfile > ../.pylintrc

