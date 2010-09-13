# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from pyarm.gui.abstract_gui import AbstractGUI
import Tkinter as tk
import numpy as np
import math

class GUI(AbstractGUI):
    "Tkinter graphical user interface."

    running = None

    arm = None
    muscle = None

    root = None
    canvas = None
    labels = {}
    label_strings = {}

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

    def __init__(self, muscle, arm):
        self.arm = arm
        self.muscle = muscle

        # Create the main window
        self.root = tk.Tk()
        self.root.resizable(False, False)

        # Set listenters (see "man bind" for more info)
        self.root.bind("<KeyPress>", self.keypress_callback)
        self.root.bind("<KeyRelease>", self.keyrelease_callback)

        # Add a callback on WM_DELETE_WINDOW event
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        # Shoulder labels
        self.labels['shoulder'] = tk.Label(self.root, text='Shoulder :')
        self.labels['shoulder'].grid(row=0, column=0, sticky='E')
        index = 1
        for label in ['shoulder_angle', 'shoulder_velocity', 'shoulder_torque']:
            self.label_strings[label] = tk.StringVar() 
            self.label_strings[label].set('-')
            self.labels[label] = tk.Label(self.root,
                                          textvariable=self.label_strings[label])
            self.labels[label].grid(row=0, column=index, sticky='W')
            index += 1

        # Elbow labels
        self.labels['elbow'] = tk.Label(self.root, text='Elbow :')
        self.labels['elbow'].grid(row=1, column=0, sticky='E')
        index = 1
        for label in ['elbow_angle', 'elbow_velocity', 'elbow_torque']:
            self.label_strings[label] = tk.StringVar() 
            self.label_strings[label].set('-')
            self.labels[label] = tk.Label(self.root,
                                          textvariable=self.label_strings[label])
            self.labels[label].grid(row=1, column=index, sticky='W')
            index += 1

        # Canvas
        self.canvas = tk.Canvas(self.root,
                                width=self.canevas_width,
                                height=self.canevas_height)
        self.canvas.grid(row=2, column=0, columnspan=4)

        self.canvas.create_rectangle((1, 1, 800, 600),
                                     fill="white",
                                     outline="black")

        # Button
        quit_button = tk.Button(self.root,
                                text="Quit",
                                command=self.quit)
        quit_button.grid(row=3, column=0, columnspan=4)
        
        self.running = True


    def quit(self):
        self.running = False
        self.root.destroy()


    def keypress_callback(self, event):
        "Update keyboard flags."

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
        "Update keyboard flags."

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

    ###########################################################################

    def update(self, input_signal, torque, acceleration):
        "Redraw the screen."
        try:
            # Update labels
            self.label_strings['shoulder_angle'].set("angle = %1.2frd (%03d°)" \
                % (self.arm.angles[0], math.degrees(self.arm.angles[0])))
            self.label_strings['shoulder_velocity'].set("velocity = %1.2frd/s" \
                % self.arm.velocities[0])
            self.label_strings['shoulder_torque'].set("torque = %03dN.m" \
                % torque[0])
            self.label_strings['elbow_angle'].set("angle = %1.2frd (%03d°)" \
                % (self.arm.angles[1], math.degrees(self.arm.angles[1])))
            self.label_strings['elbow_velocity'].set("velocity = %1.2frd/s" \
                % self.arm.velocities[1])
            self.label_strings['elbow_torque'].set("torque = %03dN.m" \
                % torque[1])

            # Update the caneva
            self.draw_shapes(input_signal)

            self.root.update_idletasks() # redraw
            self.root.update()           # process events
            
            self.take_a_screenshot()
        except tk.TclError:
            pass # to avoid errors when the window is closed


    def clear_canvas(self):
        "Clear the canvas"
        # Clear the canvas
        for tag in self.canvas.find_all():
            self.canvas.delete(tag)

        # Draw white background
        self.canvas.create_rectangle((1, 1, 800, 600),
                                     fill="white",
                                     outline="black")

    def draw_line(self, *args, **kw):
        "TODO : doc..."
        points = np.array(args[0])
        points_array = points.reshape((2, points.shape[0] / 2))
        points_array[:, 1] *= -1
        # TODO : self.canevas_height  self.winfo_height() self.winfo_reqheight()
        points_array[:, 1] += self.canvas.winfo_height()
        points = points_array.reshape(points_array.shape[0] \
                                      * points_array.shape[1])
        args = points.tolist()
        return self.canvas.create_line(args, kw)

    def draw_arc(self, x_point, y_point, radius, **kw):
        "TODO : doc..."
        radius = abs(radius)
        y_point *= -1
        y_point += self.canvas.winfo_height() # TODO
        args = (x_point + radius,
                y_point + radius,
                x_point - radius,
                y_point - radius)
        return self.canvas.create_arc(args, kw)

    def draw_circle(self, x_point, y_point, radius, **kw):
        "TODO : doc..."
        radius = abs(radius)
        y_point *= -1
        y_point += self.canvas.winfo_height() # TODO
        args = (x_point + radius,
                y_point + radius,
                x_point - radius,
                y_point - radius)
        return self.canvas.create_oval(args, kw)

    def draw_text(self, x_point, y_point, **kw):
        "TODO : doc..."
        y_point *= -1
        y_point += self.canvas.winfo_height() # TODO
        args = (x_point, y_point)
        return self.canvas.create_text(args, kw)

