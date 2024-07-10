#!/bin/bash

source $HELPER_SCRIPTS/document.sh

VERSION=$1

echo "[*] Installing allure-commandline $VERSION";

cd /tmp/
curl -sL https://repo1.maven.org/maven2/io/qameta/allure/allure-commandline/$VERSION/allure-commandline-$VERSION.tgz -o allure-commandline-$VERSION.tgz
tar -zxvf allure-commandline-$VERSION.tgz -C /opt/
ln -s /opt/allure-$VERSION/bin/allure /usr/bin/allure
rm allure-commandline-$VERSION.tgz


echo "Lastly, documenting what we added to the metadata file"
DocumentInstalledItem "allure-commandline ($(allure --version | head -n 1))"

