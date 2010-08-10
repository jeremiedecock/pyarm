#!/bin/sh

find . -name "*.pyc" -exec rm {} \;
find . -name "*.pyo" -exec rm {} \;
rm -rf screencast
rm -rf scripts
rm -rf build
rm -rf dist
rm MANIFEST
rm *.log
rm *.png
