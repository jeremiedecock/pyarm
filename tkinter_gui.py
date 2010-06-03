# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import Tkinter
import math

class GUI:

    delta_time  = 0.01                          # The state of the arm is updated at every tick_duration time (s)
    former_time = 0.
    realtime = True

    arm = None
    muscle = None

    root = None
    canv = None
    LENGTH_SCALE = 300. # px/m (pixels per meter)

    def __init__(self, muscle, arm, realtime):
        self.muscle = muscle
        self.arm = arm

        # Create the main window
        self.root = Tkinter.Tk()
        self.root.resizable(False, False)
        #self.root.bind("<Key>", self.keyboard_callback)
        self.root.bind("<KeyPress>", self.keypress_callback)
        self.root.bind("<KeyRelease>", self.keyrelease_callback)

        # Canvas
        canv = Tkinter.Canvas(self.root, width=800, height=600)
        canv.pack()

        canv.create_rectangle((2,2,199,199), fill="white", outline="black")
        canv.create_line((10,30,30,80), fill="red", width=2)
        canv.create_oval((30,10,60,30), fill="yellow", outline="cyan")
        canv.create_polygon((40,40, 55,50, 70,40, 60,55, 70,70, 55,60, 40,70, 50,55), fill="green")

        # Label
        str_var = Tkinter.StringVar() 
        label = Tkinter.Label(self.root, textvariable=str_var)
        label.pack()

        str_var.set('Label')

        # Button
        quit_button = Tkinter.Button(self.root, text="Quitter", command=self.root.quit)
        quit_button.pack()
    
    def keypress_callback(self, event):
        # ['__doc__', '__module__', 'char', 'delta', 'height', 'keycode', 'keysym', 'keysym_num', 'num', 'send_event', 'serial', 'state', 'time', 'type', 'widget', 'width', 'x', 'x_root', 'y', 'y_root']
        print "press ", event.char

    def keyrelease_callback(self, event):
        # ['__doc__', '__module__', 'char', 'delta', 'height', 'keycode', 'keysym', 'keysym_num', 'num', 'send_event', 'serial', 'state', 'time', 'type', 'widget', 'width', 'x', 'x_root', 'y', 'y_root']
        print "release ", event.char

    def keyboard_callback(self, event):
        # ['__doc__', '__module__', 'char', 'delta', 'height', 'keycode', 'keysym', 'keysym_num', 'num', 'send_event', 'serial', 'state', 'time', 'type', 'widget', 'width', 'x', 'x_root', 'y', 'y_root']
        print event.char

    def run(self):
        # The main loop
        running = True

        self.root.mainloop()

#        try:
#            while running:
#                # Get events
#
#
#                # Update thetas (physics)
##                self.armModel.tick(input)
#
##                theta = self.armModel.getTheta()
##                omega = self.armModel.getOmega()
##                alpha = self.armModel.getAlpha()
##                tau   = self.armModel.getTau()
#
#                # Update the caneva
#                self.root.update_idletasks() # redraw
#                self.root.update() # process events
#        except Tkinter.TclError:
#            pass # to avoid errors when the window is closed

