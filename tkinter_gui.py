# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import Tkinter as tk
import numpy as np
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

    initial_angle = 0
    #initial_angle = math.pi / 2

    canevas_width = 800
    canevas_height = 600
    LENGTH_SCALE = 450. # px/m (pixels per meter)

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

    def draw_shapes(self, shoulder_angle, elbow_angle):
        # TODO : only delete moving parts (not the background rectangle of example)
        for tag in self.canvas.find_all():
            self.canvas.delete(tag)

        self.canvas.create_rectangle((1,1,800,600), fill="white", outline="black")

        # Draw the initial angle arrow
        arrow_point1 = np.array([10, 10]) + self.LENGTH_SCALE / 10
        arrow_point2 = np.array([math.cos(self.initial_angle),  \
                                 math.sin(self.initial_angle)]) \
                       * self.LENGTH_SCALE / 10 + arrow_point1
        arrow_point3 = np.array([math.cos(self.initial_angle + math.pi/2),  \
                                 math.sin(self.initial_angle + math.pi/2)]) \
                       * self.LENGTH_SCALE / 20 + arrow_point1
        self.canvas.create_line(arrow_point1.tolist() + arrow_point2.tolist())
        self.canvas.create_line(arrow_point1.tolist() + arrow_point3.tolist())

        #####
        p0 = np.array([self.canevas_width, self.canevas_height]) / 2.
        p1 = np.array([math.cos(self.initial_angle + shoulder_angle),  \
                       math.sin(self.initial_angle + shoulder_angle)]) \
             * self.arm.upperarm_length * self.LENGTH_SCALE + p0
        p2 = np.array([math.cos(self.initial_angle + shoulder_angle + elbow_angle),  \
                       math.sin(self.initial_angle + shoulder_angle + elbow_angle)]) \
             * self.arm.upperarm_length * self.LENGTH_SCALE + p1

        # Draw angles
        shoulder_oval_point1 = p0 - 25
        shoulder_oval_point2 = p0 + 25
        self.canvas.create_arc(shoulder_oval_point1.tolist() + shoulder_oval_point2.tolist(),
                               start=0, extent=270, fill="red")

        elbow_oval_point1 = p1 - 25
        elbow_oval_point2 = p1 + 25
        self.canvas.create_arc(elbow_oval_point1.tolist() + elbow_oval_point2.tolist(),
                               start=0, extent=270, fill="red")

        angle_point1 = p0
        angle_point2 = np.array([math.cos(self.initial_angle),  \
                                 math.sin(self.initial_angle)]) \
                       * 30 + p0
        angle_point3 = p1
        angle_point4 = np.array([math.cos(self.initial_angle + shoulder_angle),  \
                                 math.sin(self.initial_angle + shoulder_angle)]) \
                       * 30 + p1

        self.canvas.create_line(angle_point1.tolist() + angle_point2.tolist(), width=1)
        self.canvas.create_line(angle_point3.tolist() + angle_point4.tolist(), width=1)

        # Draw angles bounds

        # Draw limbs
        self.canvas.create_line(p0.tolist() + p1.tolist(), fill="black", width=5)
        self.canvas.create_line(p1.tolist() + p2.tolist(), fill="black", width=5)

        # Draw joints
        if hasattr(self.muscle, 'A'):
            shoulder_point1 = p0 - self.muscle.A[0,0] * self.LENGTH_SCALE
            shoulder_point2 = p0 + self.muscle.A[0,0] * self.LENGTH_SCALE
            shoulder_point3 = p0 - self.muscle.A[4,0] * self.LENGTH_SCALE
            shoulder_point4 = p0 + self.muscle.A[4,0] * self.LENGTH_SCALE
            self.canvas.create_oval(shoulder_point1.tolist() + shoulder_point2.tolist())
            self.canvas.create_oval(shoulder_point3.tolist() + shoulder_point4.tolist())

            elbow_point1 = p1 - self.muscle.A[2,1] * self.LENGTH_SCALE
            elbow_point2 = p1 + self.muscle.A[2,1] * self.LENGTH_SCALE
            elbow_point3 = p1 - self.muscle.A[4,1] * self.LENGTH_SCALE
            elbow_point4 = p1 + self.muscle.A[4,1] * self.LENGTH_SCALE
            self.canvas.create_oval(elbow_point1.tolist() + elbow_point2.tolist())
            self.canvas.create_oval(elbow_point3.tolist() + elbow_point4.tolist())

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
                self.draw_shapes(*theta)

                self.root.update_idletasks() # redraw
                self.root.update() # process events
        except tk.TclError:
            pass # to avoid errors when the window is closed

