#!/bin/bash
################################################################################
##  File:  azure-cli.sh
##  Team:  CI-Platform
##  Desc:  Installed Azure CLI (az)
################################################################################

# Source the helpers for use with the script
source $HELPER_SCRIPTS/document.sh

LSB_CODENAME=$(lsb_release -cs)

echo '***** LSB_CODENAME:' $LSB_CODENAME
# Install Azure CLI
echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $LSB_CODENAME main" | tee /etc/apt/sources.list.d/azure-cli.list

# Download and install the Microsoft signing key
curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/microsoft.asc.gpg > /dev/null

# Update and install the Azure CLI package
apt-get update
apt-get install -y --no-install-recommends apt-transport-https azure-cli

# Run tests to determine that the software installed as expected
echo "Testing to make sure that script performed as expected, and basic scenarios work"
if ! command -v az; then
    echo "azure-cli was not installed"
    exit 1
fi

# Document what was added to the image
DocumentInstalledItem "Azure CLI ($(az -v | head -n 1))"

# Setup Azure Extension directory
echo "AZURE_EXTENSION_DIR=/usr/local/lib/azureExtensionDir" | tee -a /etc/environment
mkdir -p /usr/local/lib/azureExtensionDir
