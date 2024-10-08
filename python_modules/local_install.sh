#!/bin/sh

echo "Installing parametricDesign."
export PD_VERSION=$(python version.py)
export SYS_ARCH=$(dpkg --print-architecture)
export PD_DEB_PKG_FOLDER="./debian-pkg"
export USR_LOCAL="/usr/local"
export PD_INSTALLATION_TARGET="${PD_DEB_PKG_FOLDER}${USR_LOCAL}/tmp"
echo "$PD_VERSION" > ./pd_installation_target.txt
echo "$SYS_ARCH" >> ./pd_installation_target.txt
echo "$PD_DEB_PKG_FOLDER" >> ./pd_installation_target.txt
echo "$PD_INSTALLATION_TARGET" >> ./pd_installation_target.txt
echo "$USR_LOCAL" >> ./pd_installation_target.txt
rm -rf $PD_DEB_PKG_FOLDER
mkdir $PD_DEB_PKG_FOLDER

pip3 install . -v --quiet --log ./installation_report.log --upgrade --target=$PD_INSTALLATION_TARGET
python prepare_deb_pkg.py
# Create debian package
dpkg-deb --build $PD_DEB_PKG_FOLDER
dpkg-name --overwrite "$PD_DEB_PKG_FOLDER.deb"
PD_DEB_PKG=$(ls -t *.deb | head -1)
echo "New Debian package: $PD_DEB_PKG"
echo "Clean temporary files."
rm -r $PD_DEB_PKG_FOLDER
echo "Install package."
sudo dpkg -i "$PD_DEB_PKG"
echo "$PD_DEB_PKG" >> ./pd_installation_target.txt
echo "Remove package files after installation."
rm -vi *.deb


