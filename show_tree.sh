#!/bin/bash

# Function to display a directory tree with exclusions
display_tree() {
    local dir=$1
    local exclude=$2
    echo "Directory structure for ${dir}:"
    tree "${dir}" -I "${exclude}" 2>/dev/null || echo "Directory ${dir} not found."
    echo ""
}

# Display the virtual environment, excluding most details
display_tree "priceTrackEnv" "bin|include|lib|lib64|pyvenv.cfg"

# Display the botFiles folder, excluding unnecessary files
display_tree "botFiles" "__pycache__|*.pyc"

# Display the data folder
display_tree "../data" "__pycache__|*.pyc"

