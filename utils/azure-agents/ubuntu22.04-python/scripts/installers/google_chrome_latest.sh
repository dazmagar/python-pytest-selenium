#!/bin/bash

source $HELPER_SCRIPTS/document.sh

echo "[*] Installing Google Chrome";

cd /tmp/
CHROME_URL="https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
CHROME_DEB="google-chrome-stable_current_amd64.deb"

# Download Google Chrome .deb package
curl -sL $CHROME_URL -o $CHROME_DEB

# Install Google Chrome
dpkg -i $CHROME_DEB || apt-get install -f -y

# Run tests to confirm installation
if ! command -v google-chrome; then
    echo "Google Chrome was not installed correctly"
    exit 1
fi

# Clean up
rm $CHROME_DEB

# Documenting the installation
CHROME_VERSION=$(google-chrome --version)
echo "Lastly, documenting what we added to the metadata file"
DocumentInstalledItem "Google Chrome $CHROME_VERSION"
