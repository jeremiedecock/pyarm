# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import Tkinter
import math

class GUI:

    armModel = None
    root = None
    canv = None
    background_color = None
    foreground_color = None
    text1 = None
    text2 = None
    line1 = None
    line2 = None
    LENGTH_SCALE = 300. # px/m (pixels per meter)

    def __init__(self, armModel):
        self.armModel = armModel

        # Create the main window
        root = Tkinter.Tk()

        canv = Tkinter.Canvas(root, width=800, height=600)
        canv.pack()


        self.window = sf.RenderWindow(sf.VideoMode(800, 600), "pyArm")



        self.line1 = sf.Shape.Line(0, 0, 0, self.armModel.getBonesLength()[0] * self.LENGTH_SCALE, 10, self.background_color, 2, self.foreground_color)
        self.centerLine(self.line1)

        self.line2 = sf.Shape.Line(0, 0, 0, self.armModel.getBonesLength()[1] * self.LENGTH_SCALE, 10, self.background_color, 2, self.foreground_color)
        self.centerLine(self.line2)

    def draw(self):
        canv.create_rectangle((2,2,99,99),fill="white",outline="blue")
        canv.create_line((10,30,30,80),fill="red",width=2)
        canv.create_oval((30,10,60,30),fill="yellow",outline="cyan")

    def run(self):

        #root.mainloop()

        # The main loop
        running = True

        try:
            while running:
                # Get events


                # Update thetas (physics)
                self.armModel.tick(input)

                theta = self.armModel.getTheta()
                omega = self.armModel.getOmega()
                alpha = self.armModel.getAlpha()
                tau   = self.armModel.getTau()

                # Update the caneva
                for i in range(len(items)):
                    items[i] = items[i]()
                    root.update_idletasks() # redraw
                root.update() # process events
        except TclError:
            pass # to avoid errors when the window is closed


