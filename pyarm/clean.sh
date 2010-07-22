#!/bin/sh

find . -name "*.pyc" -exec rm {} \;
find . -name "*.pyo" -exec rm {} \;
rm -rf screencast
rm *.log
rm *.png
