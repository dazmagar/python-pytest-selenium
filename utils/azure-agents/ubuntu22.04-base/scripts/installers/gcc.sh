#!/bin/bash
################################################################################
##  File:  gcc.sh
##  Team:  CI-Platform
##  Desc:  Installs GNU C++
################################################################################

# Source the helpers for use with the script
source $HELPER_SCRIPTS/document.sh

# Install GNU C++ compiler
apt-get update
apt-get install -y gcc g++

# Проверяем установку и выводим версию
gcc_version=$(gcc --version | head -n 1)
gpp_version=$(g++ --version | head -n 1)
echo "Testing to make sure that script performed as expected, and basic scenarios work"
if [ -z "$gcc_version" ] || [ -z "$gpp_version" ]; then
    echo "GNU C/C++ compiler was not installed"
    exit 1
else
    echo "Installed $gcc_version"
    echo "Installed $gpp_version"
fi

# Document what was added to the image
echo "Lastly, documenting what we added to the metadata file"
DocumentInstalledItem "GCC: $gcc_version"
DocumentInstalledItem "G++: $gpp_version"
