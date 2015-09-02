#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import unittest
import os
import sys

dirname = os.path.dirname(__file__)
if dirname == '':
    dirname = '.'

dirname = os.path.realpath(dirname)
updir = os.path.split(dirname)[0]
if updir not in sys.path:
    sys.path.append(updir)

###

import plot_figs

class PlotFigsTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_main(self):
        try:
            plot_figs.main()
        except:
            self.fail()

    def tearDown(self):
        # Remove files
        files = ("arm_Kambara_c_forearm.png", "muscle_Kambara_k.png",
                 "muscle_Kambara_lr.png", "muscle_Li_fa.png",
                 "muscle_Li_fl.png", "muscle_Li_nf.png",
                 "muscle_Mitrovic_lm.png", "muscle_Mitrovic_v.png",
                 "arm_Mitrovic_c_forearm.png", "muscle_Kambara_lm.png",
                 "muscle_Kambara_v.png", "muscle_Li_fe.png",
                 "muscle_Li_fv.png", "muscle_Mitrovic_k.png",
                 "muscle_Mitrovic_lr.png")
        try:
            list(map(os.remove, files))
        except:
            pass

###

def test_suite():
    tests = [unittest.makeSuite(PlotFigsTest)]
    return unittest.TestSuite(tests)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

