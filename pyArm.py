#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import sfmlGui as view
#import simpleDynamicsModel as model
import mitrovicModel as model

# Main #########################################################################

def main():
    armModel = model.ArmModel()
    gui = view.GUI(armModel)
    gui.run()

################################################################################

if __name__ == '__main__':
    main()
    
