# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import Tkinter as tk
import numpy as np
import math
import time
import fig
import os

class GUI:
    "Tkinter graphical user interface."

    # The state of the arm is updated at every tick_duration time (s)
    delta_time = 0.005
    #delta_time = 0.01 
    former_time = 0.
    init_time = 0.

    realtime = True
    screencast = None

    running = True

    agent = None
    arm = None
    muscle = None

    root = None
    canvas = None
    str_var1 = None
    str_var2 = None

    initial_angle = 0
    #initial_angle = -math.pi / 2

    canevas_width = 800
    canevas_height = 600
    scale = 450. # px/m (pixels per meter)

    keyboard_flags = [0, 0, 0, 0, 0, 0]

    draw_angles_bounds = True
    draw_angles = True
    draw_joints = True
    draw_muscles = True

    def __init__(self, muscle, arm, agent=None, realtime=False,
                 screencast=False):
        self.arm = arm
        self.muscle = muscle
        self.agent = agent

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
        self.canvas = MathCanvas(self.root,
                                 width=self.canevas_width,
                                 height=self.canevas_height)
        self.canvas.pack()

        self.canvas.create_rectangle((1, 1, 800, 600),
                                     fill="white",
                                     outline="black")

        # Button
        quit_button = tk.Button(self.root,
                                text="Quit",
                                command=self.root.destroy)
        quit_button.pack()

        self.realtime = realtime
        self.screencast = screencast

        self.former_time = time.time()         # Former time (s)
        self.init_time = self.former_time      # Initial time (s)

        fig.subfig('dtime',
                   title='Time',
                   xlabel='time (s)',
                   ylabel='delta time (s)')
        fig.subfig('input signal',
                   title='Signal',
                   xlabel='time (s)',
                   ylabel='signal',
                   ylim=[-0.1, 1.1])

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
    
        # Compute limb points and angles ########

        global_shoulder_angle = self.initial_angle + shoulder_angle
        global_elbow_angle = global_shoulder_angle + elbow_angle

        shoulder_point = np.array([self.canevas_width, self.canevas_height]) / 2.
        elbow_point = np.array([math.cos(global_shoulder_angle),  \
                       math.sin(global_shoulder_angle)]) \
             * self.arm.upperarm_length * self.scale + shoulder_point
        wrist_point = np.array([math.cos(global_elbow_angle),  \
                       math.sin(global_elbow_angle)]) \
             * self.arm.upperarm_length * self.scale + elbow_point

        # Draw parts ############################

        # Clear the canvas
        # TODO : only delete moving parts (eg. not the background rectangle of
        #        example)
        for tag in self.canvas.find_all():
            self.canvas.delete(tag)

        # Draw white background
        self.canvas.create_rectangle((1, 1, 800, 600),
                                     fill="white",
                                     outline="black")

        # Draw angles bounds
        if self.draw_angles_bounds:
            # Shoulder
            angle_start = math.degrees(self.initial_angle + self.arm.theta_bounds[0]['min'])
            angle_extent = math.degrees(self.arm.theta_bounds[0]['max'] - self.arm.theta_bounds[0]['min'])
            self.canvas.draw_arc(shoulder_point[0].tolist(),
                                 shoulder_point[1].tolist(),
                                 25,
                                 start=angle_start,
                                 extent=angle_extent,
                                 outline="white",
                                 fill="gray")

            # Elbow
            angle_start = math.degrees(global_shoulder_angle + self.arm.theta_bounds[1]['min'])
            angle_extent = math.degrees(self.arm.theta_bounds[1]['max'] - self.arm.theta_bounds[1]['min'])
            self.canvas.draw_arc(elbow_point[0].tolist(),
                                 elbow_point[1].tolist(),
                                 25,
                                 start=angle_start,
                                 extent=angle_extent,
                                 outline="white",
                                 fill="gray")

        # Draw angles
        if self.draw_angles:
            # Shoulder arc angle
            self.canvas.draw_arc(shoulder_point[0].tolist(),
                                 shoulder_point[1].tolist(),
                                 25,
                                 start=math.degrees(self.initial_angle),
                                 extent=math.degrees(shoulder_angle))

            # Elbow arc angle
            self.canvas.draw_arc(elbow_point[0].tolist(),
                                 elbow_point[1].tolist(),
                                 25,
                                 start=math.degrees(global_shoulder_angle),
                                 extent=math.degrees(elbow_angle))

            # Shoulder initial line
            point1 = shoulder_point
            point2 = np.array([math.cos(self.initial_angle), 
                               math.sin(self.initial_angle)]) \
                     * 30 + shoulder_point
            self.canvas.draw_line(point1.tolist() + point2.tolist(),
                                    width=1)

            # Elbow initial line
            point1 = elbow_point
            point2 = np.array([math.cos(global_shoulder_angle), 
                               math.sin(global_shoulder_angle)]) \
                     * 30 + elbow_point
            self.canvas.draw_line(point1.tolist() + point2.tolist(),
                                    width=1)

        # Draw limbs
        self.canvas.draw_line(shoulder_point.tolist() + elbow_point.tolist(),
                                fill="black",
                                width=5)
        self.canvas.draw_line(elbow_point.tolist() + wrist_point.tolist(),
                                fill="black",
                                width=5)

        # Draw joints
        if self.draw_joints and hasattr(self.muscle, 'A'):
            # Shoulder
            self.canvas.draw_circle(shoulder_point[0].tolist(),
                                    shoulder_point[1].tolist(),
                                    self.muscle.A[0, 0] * self.scale)
            self.canvas.draw_circle(shoulder_point[0].tolist(),
                                    shoulder_point[1].tolist(),
                                    self.muscle.A[4, 0] * self.scale)

            # Elbow
            self.canvas.draw_circle(elbow_point[0].tolist(),
                                    elbow_point[1].tolist(),
                                    self.muscle.A[2, 1] * self.scale)
            self.canvas.draw_circle(elbow_point[0].tolist(),
                                    elbow_point[1].tolist(),
                                    self.muscle.A[4, 1] * self.scale)

    def run(self):
        # The main loop
        try:
            iteration = 0

            alpha = [0., 0.]
            omega = [0., 0.]
            theta = [0., 0.]
            #tau = [0., 0.] ###

            #import xcsfpython as xp ###
            #xcsf = xp.XCSF(host='127.0.0.1', configFilePath='xcsf.ini') ###
            #xcsf.initialize(6, 2) ###

            while self.running:
                iteration += 1

                #state = np.array([xcsf.norm(tau[0], self.arm.taumin, self.arm.taumax),
                #                  xcsf.norm(tau[1], self.arm.taumin, self.arm.taumax),
                #                  xcsf.norm(omega[0], self.arm.omegamin, self.arm.omegamax),
                #                  xcsf.norm(omega[1], self.arm.omegamin, self.arm.omegamax),
                #                  xcsf.norm(theta[0], self.arm.theta_bounds[0]['min'], self.arm.theta_bounds[0]['max']),
                #                  xcsf.norm(theta[1], self.arm.theta_bounds[1]['min'], self.arm.theta_bounds[1]['max'])]) ###

                # Compute delta time
                current_time = time.time()

                if self.realtime:
                    self.delta_time = current_time - self.former_time
            
                fig.append('dtime', self.delta_time)

                elapsed_time = current_time - self.init_time

                # Get input signals
                input_signal = None
                if self.agent == None:
                    input_signal = [float(flag) for flag in self.keyboard_flags]
                else:
                    input_signal = self.agent.get_action(alpha=alpha,
                                                         omega=omega,
                                                         theta=theta,
                                                         time=elapsed_time)
            
                fig.append('input signal', input_signal)

                # Update thetas (physics)
                tau = self.muscle.update(input_signal,
                                         self.arm.theta,
                                         self.delta_time)
                alpha, omega, theta = self.arm.update(tau, self.delta_time)

                # Update clock
                self.former_time = current_time

                #xcsf.update(state, np.array(alpha)) ###

                # Update the caneva
                self.str_var1.set("Shoulder : angle = %1.2frd (%03d°)     velocity = %1.2frd/s     acceleration = %1.2frd/s/s     torque = %03dN.m" % (theta[0], math.degrees(theta[0]), omega[0], alpha[0], tau[0]))
                self.str_var2.set("Elbow : angle = %1.2frd (%03d°)     velocity = %1.2frd/s     acceleration = %1.2frd/s/s     torque = %03dN.m" % (theta[1], math.degrees(theta[1]), omega[1], alpha[1], tau[1]))
                self.draw_shapes(*theta)

                self.root.update_idletasks() # redraw
                self.root.update() # process events

                if self.screencast:
                    self.canvas.postscript(file='%s/%05d.ps' % ('screencast', iteration), colormode='color')
                    os.system('gs -sDEVICE=jpeg -sOutputFile=%(path)s/%(iteration)05d.jpeg -dNOPAUSE -q -dBATCH %(path)s/%(iteration)05d.ps' % {'iteration': iteration, 'path': 'screencast'})
        except tk.TclError:
            pass # to avoid errors when the window is closed


class MathCanvas(tk.Canvas):
    "A canvas where the origin is placed at the bottom left corner."

    def draw_line(self, *args, **kw):
        "TODO : doc..."
        points = np.array(args[0])
        points_array = points.reshape((2, points.shape[0] / 2))
        points_array[:, 1] *= -1
        points_array[:, 1] += self.winfo_height()      # TODO : self.canevas_height  self.winfo_height()   self.winfo_reqheight()
        points = points_array.reshape(points_array.shape[0] \
                                      * points_array.shape[1])
        args = points.tolist()
        return self.create_line(args, kw)

    def draw_arc(self, x_point, y_point, radius, **kw):
        "TODO : doc..."
        radius = abs(radius)
        y_point *= -1
        y_point += self.winfo_height() # TODO
        args = (x_point + radius,
                y_point + radius,
                x_point - radius,
                y_point - radius)
        return self.create_arc(args, kw)

    def draw_circle(self, x_point, y_point, radius, **kw):
        "TODO : doc..."
        radius = abs(radius)
        y_point *= -1
        y_point += self.winfo_height() # TODO
        args = (x_point + radius,
                y_point + radius,
                x_point - radius,
                y_point - radius)
        return self.create_oval(args, kw)

    def draw_text(self, x_point, y_point, **kw):
        "TODO : doc..."
        y_point *= -1
        y_point += self.winfo_height() # TODO
        args = (x_point, y_point)
        return self.create_text(args, kw)

