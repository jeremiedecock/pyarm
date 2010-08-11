#!/bin/sh

NAME=pyarm
VERSION=$(cat VERSION)
DIST_DIR=dist

rm -rf debian

mkdir -p      debian/usr/bin
cp $NAME.py   debian/usr/bin/$NAME
chmod 755     debian/usr/bin/$NAME

# TODO
mkdir -p      debian/usr/local/lib/python2.6/dist-packages
cp -r pyarm   debian/usr/local/lib/python2.6/dist-packages
chmod 644     $(find debian/usr/local/lib -type f)

mkdir -p      debian/usr/share/doc/$NAME/
cp COPYING    debian/usr/share/doc/$NAME/copyright
chmod 644     debian/usr/share/doc/$NAME/copyright

mkdir -p debian/DEBIAN

# section list : http://packages.debian.org/stable/
cat > debian/DEBIAN/control << EOF
Package: $NAME
Version: $VERSION
Section: science
Priority: optional
Maintainer: Jérémie DECOCK <gremy@tuxfamily.org>
Architecture: all
Depends: python (>= 2.5), python-numpy, python-matplotlib
Description: A robotic arm model and simulator
EOF

fakeroot dpkg-deb -b debian

mkdir -p $DIST_DIR
mv debian.deb $DIST_DIR/${NAME}_${VERSION}_all.deb
