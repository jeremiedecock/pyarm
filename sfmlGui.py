#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from PySFML import sf
import math

class GUI:

    armModel = None
    window = None
    background_color = None
    foreground_color = None
    text1 = None
    text2 = None
    line1 = None
    line2 = None
    LENGTH_SCALE = 1000.

    def __init__(self, armModel):
        self.armModel = armModel

        # Create the main window
        self.window = sf.RenderWindow(sf.VideoMode(800, 600), "pyArm")

        self.background_color = sf.Color(255, 255, 255, 255)
        self.foreground_color = sf.Color(0, 0, 0, 255)

        # Create a graphical elements to display
        #font = sf.Font()
        #font.LoadFromFile('FreeSans.ttf', 11, 'utf8')
        #font.LoadFromFile('/home/decock/git_pub/pyArm/FreeSans.ttf')

        #self.text1 = sf.String("", font, 11)
        self.text1 = sf.String("", Size=16)
        self.text1.SetColor(self.foreground_color)
        self.text1.SetPosition(20, 10)

        #self.text2 = sf.String("", font, 11)
        self.text2 = sf.String("", Size=16)
        self.text2.SetColor(self.foreground_color)
        self.text2.SetPosition(20, 40)

        self.line1 = sf.Shape.Line(0, 0, 0, self.armModel.getL1() * self.LENGTH_SCALE, 10, self.background_color, 2, self.foreground_color)
        self.centerLine(self.line1)

        self.line2 = sf.Shape.Line(0, 0, 0, self.armModel.getL2() * self.LENGTH_SCALE, 10, self.background_color, 2, self.foreground_color)
        self.centerLine(self.line2)

    def centerLine(self, line):
        screen_center = (self.window.GetWidth() / 2, self.window.GetHeight() / 2)
        line.SetPosition(*screen_center)

    def translateLine(self, line, line_ref):
        p0   = line_ref.TransformToGlobal(*line_ref.GetPointPosition(0))
        p1   = line_ref.TransformToGlobal(*line_ref.GetPointPosition(1))
        vect = (p1[0]-p0[0] , p1[1]-p0[1])

        line.Move(*vect)

    def updateShapes(self):
        # Line 1
        self.line1.SetRotation(math.degrees(self.armModel.getTheta1()))

        # Line 2
        self.centerLine(self.line2)
        self.line2.SetRotation(math.degrees(self.armModel.getTheta1()))
        self.line2.SetRotation(math.degrees(self.armModel.getTheta2()))
        self.translateLine(self.line2, self.line1)

    def run(self):
        window_input = self.window.GetInput()

        # The main loop
        running = True

        while running:
            # Get events
            event = sf.Event()
            while self.window.GetEvent(event):
                if event.Type == sf.Event.Closed:
                    running = False

            input = (window_input.IsKeyDown(sf.Key.Numpad1), window_input.IsKeyDown(sf.Key.Numpad2), window_input.IsKeyDown(sf.Key.Numpad4), window_input.IsKeyDown(sf.Key.Numpad5))
            #print input

            # Update thetas (physics)
            self.armModel.tick(input)

            # Update the window
            self.updateShapes()
            self.text1.SetText("Theta 1 = %1.2frd (%03d°)   Omega 1 = %1.2frd/s   Alpha 1 = %1.2frd/s/s   Tau 1 = %03dN.m" % (self.armModel.getTheta1(), math.degrees(self.armModel.getTheta1()), self.armModel.getOmega1(), self.armModel.getAlpha1(), self.armModel.getTau1()))
            self.text2.SetText("Theta 2 = %1.2frd (%03d°)   Omega 2 = %1.2frd/s   Alpha 2 = %1.2frd/s/s   Tau 2 = %03dN.m" % (self.armModel.getTheta2(), math.degrees(self.armModel.getTheta2()), self.armModel.getOmega2(), self.armModel.getAlpha2(), self.armModel.getTau2()))

            self.window.Clear(self.background_color)

            self.window.Draw(self.text1)
            self.window.Draw(self.text2)
            self.window.Draw(self.line1)
            self.window.Draw(self.line2)

            self.window.Display()

