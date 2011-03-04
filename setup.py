#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from distutils.core import setup
import subprocess
import os
import shutil

CLASSIFIERS = ['Development Status :: 4 - Beta',
               'Environment :: Console',
               'Environment :: X11 Applications',
               'Intended Audience :: Science/Research',
               'License :: OSI Approved :: MIT License',
               'Operating System :: POSIX :: Linux',
               'Programming Language :: Python',
               'Topic :: Scientific/Engineering :: Physics',
               'Topic :: Scientific/Engineering :: Artificial Intelligence']

PACKAGES = ['pyarm',
            'pyarm.agent',
            'pyarm.gui',
            'pyarm.model',
            'pyarm.model.arm',
            'pyarm.model.kinematics',
            'pyarm.model.muscle']

README_FILE = open('README', 'r')

# Prepare scripts ###########

# The list of scripts we want to export in the distrib ({'src': 'dest', ...}).
SCRIPTS = {'pyarm.py' : os.path.join('scripts', 'pyarm')}

for source, dest in SCRIPTS.iteritems():
    try:
        os.mkdir(os.path.dirname(dest))
    except OSError:
        pass # TODO

    try:
        shutil.copyfile(source, dest)
    except IOError:
        pass # TODO


# Don't use unicode strings in setup arguments or bdist_rpm will fail.
setup(author='Jeremie DECOCK',
      author_email='jd.jdhp@gmail.com',
      # See :  http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=CLASSIFIERS,
      description='A robotic arm model and simulator.',
      license='MIT license',
      long_description=README_FILE.read(),
      maintainer='Jeremie DECOCK',
      maintainer_email='jd.jdhp@gmail.com',
      name='pyarm',
      packages=PACKAGES,
      platforms=['Linux'],
      requires=['numpy', 'matplotlib'],
      scripts=SCRIPTS.values(),
      url='http://code.google.com/p/pyarm/',
      version='0.1.3')

README_FILE.close()
