#!/usr/bin/env bash

# Define directories to be deleted.
pkg="pdvalidate"
outdirs=("build" "dist" "${pkg}.egg-info")

# Delete current build/dist directories.
printf "\nDeleting build directories ...\n"
for d in ${outdirs[@]}; do
    if [ -d ${d} ]; then
        printf "Deleting %s\n" "${d}"
        rm -rf ./"${d}"
    fi
done
printf "Done.\n\n"

# Create requirements file.
printf "Creating the requirements file ...\n"
pipreqs --force --use-local ./
printf "Done.\n\n"

# Create the wheel install file.
printf "Creating source dist ...\n"
./setup.py bdist_wheel
printf "Done.\n\n"

# Copy the extraction script into ./dist
#printf "Copying the extraction script to ./dist ...\n"
#cp ./extract.sh ./dist
#printf "Done.\n\n"

printf "Setup complete.\n\n"

