#!/bin/sh

egrep "^@" article.bib | sed "s/^@.*{//g"
