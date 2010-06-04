# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import Tkinter as tk
import math
import time
import fig

class GUI:

    delta_time  = 0.01                          # The state of the arm is updated at every tick_duration time (s)
    former_time = 0.
    realtime = True

    running = True

    arm = None
    muscle = None

    root = None
    canvas = None
    str_var1 = None
    str_var2 = None

    points = None
    canevas_width = 800
    canevas_height = 600
    LENGTH_SCALE = 300. # px/m (pixels per meter)

    keyboard_flags = [0, 0, 0, 0, 0, 0]

    def __init__(self, muscle, arm, realtime):
        self.muscle = muscle
        self.arm = arm

        # Create the main window
        self.root = tk.Tk()
        self.root.resizable(False, False)

        # Set listenters (see "man bind" for more info)
        self.root.bind("<KeyPress>", self.keypress_callback)
        self.root.bind("<KeyRelease>", self.keyrelease_callback)

        # Label 1
        self.str_var1 = tk.StringVar() 
        label1 = tk.Label(self.root, textvariable=self.str_var1)
        label1.pack()

        self.str_var1.set('-')

        # Label 2
        self.str_var2 = tk.StringVar() 
        label2 = tk.Label(self.root, textvariable=self.str_var2)
        label2.pack()

        self.str_var2.set('-')

        # Canvas
        self.canvas = tk.Canvas(self.root, width=self.canevas_width, height=self.canevas_height)
        self.canvas.pack()

        self.canvas.create_rectangle((1,1,800,600), fill="white", outline="black")

        # Button
        quit_button = tk.Button(self.root, text="Quit", command=self.quit_callback)
        quit_button.pack()

        self.realtime = realtime
        self.former_time = time.time()         # Former time (s)

    def __del__(self):
        fig.show()
    
    def quit_callback(self):
        self.running = False

    def keypress_callback(self, event):
        if event.char == '1':
            self.keyboard_flags[0] = 1
        elif event.char == '2':
            self.keyboard_flags[1] = 1
        elif event.char == '3':
            self.keyboard_flags[2] = 1
        elif event.char == '4':
            self.keyboard_flags[3] = 1
        elif event.char == '5':
            self.keyboard_flags[4] = 1
        elif event.char == '6':
            self.keyboard_flags[5] = 1

    def keyrelease_callback(self, event):
        if event.char == '1':
            self.keyboard_flags[0] = 0
        elif event.char == '2':
            self.keyboard_flags[1] = 0
        elif event.char == '3':
            self.keyboard_flags[2] = 0
        elif event.char == '4':
            self.keyboard_flags[3] = 0
        elif event.char == '5':
            self.keyboard_flags[4] = 0
        elif event.char == '6':
            self.keyboard_flags[5] = 0

    def update_shapes_position(self, shoulder_angle, elbow_angle):
        p0 = (self.canevas_width / 2., self.canevas_height / 2.)
        p1 = (p0[0] + math.cos(shoulder_angle) * self.arm.upperarm_length * self.LENGTH_SCALE,
              p0[1] + math.sin(shoulder_angle) * self.arm.upperarm_length * self.LENGTH_SCALE)
        p2 = (p1[0] + math.cos(shoulder_angle + elbow_angle) * self.arm.forearm_length * self.LENGTH_SCALE,
              p1[1] + math.sin(shoulder_angle + elbow_angle) * self.arm.forearm_length * self.LENGTH_SCALE)
        self.points  = (p0, p1, p2)

    def draw_shapes(self):
        # TODO : optimiser l'affichage (le nb de FPS chute très vite), surveiller consomation memoire
        for tag in self.canvas.find_all():
            self.canvas.delete(tag)

        self.canvas.create_rectangle((1,1,800,600), fill="white", outline="black")

        self.canvas.create_line(self.points[0] + self.points[1], fill="black", width=5)
        self.canvas.create_line(self.points[1] + self.points[2], fill="black", width=5)

        #self.canvas.create_oval(self.points[0] + (20, 20), outline="black")

    def run(self):
        # The main loop
        try:
            while self.running:
                # Get events

                # Compute delta time
                current_time = time.time()

                if self.realtime:
                    self.delta_time = current_time - self.former_time

                # Update thetas (physics)
                input = self.keyboard_flags
                tau = self.muscle.update(input, self.arm.theta, self.delta_time)
                alpha, omega, theta = self.arm.update(tau, self.delta_time)

                # Update clock
                self.former_time = current_time

                # Update the caneva
                self.str_var1.set("Shoulder : angle = %1.2frd (%03d°)     velocity = %1.2frd/s     acceleration = %1.2frd/s/s     torque = %03dN.m" % (theta[0], math.degrees(theta[0]), omega[0], alpha[0], tau[0]))
                self.str_var2.set("Elbow : angle = %1.2frd (%03d°)     velocity = %1.2frd/s     acceleration = %1.2frd/s/s     torque = %03dN.m" % (theta[1], math.degrees(theta[1]), omega[1], alpha[1], tau[1]))
                self.update_shapes_position(*theta)
                self.draw_shapes()

                self.root.update_idletasks() # redraw
                self.root.update() # process events
        except tk.TclError:
            pass # to avoid errors when the window is closed

