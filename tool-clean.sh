#!/bin/sh

find . -name "*.pyc" -exec rm {} \;
find . -name "*.pyo" -exec rm {} \;
rm -rf screencast
rm -rf scripts
rm -rf build
rm -rf dist
rm MANIFEST
rm -rf pyarm_logs
rm -rf pyarm_figs
# Debian related files
rm -rf build-stamp
rm -rf debian/files
rm -rf debian/pyarm.postinst.debhelper
rm -rf debian/pyarm.postrm.debhelper
rm -rf debian/pyarm.prerm.debhelper
rm -rf debian/pyarm.substvars
rm -rf debian/pyarm/
