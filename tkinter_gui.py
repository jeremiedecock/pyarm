# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import Tkinter as tk
import numpy as np
import math

class GUI:
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
        self.canvas = MathCanvas(self.root,
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

    def draw_shapes(self, input_signal):
        "Draw shapes (arm, muscles, ...) in the canvas."
    
        # Compute limb points and angles ########

        shoulder_angle = self.arm.angles[0]
        elbow_angle = self.arm.angles[1]

        global_shoulder_angle = self.initial_angle + shoulder_angle
        global_elbow_angle = global_shoulder_angle + elbow_angle

        shoulder_point = np.array([self.canevas_width, self.canevas_height]) / 2.
        elbow_point = np.array([math.cos(global_shoulder_angle),
                                math.sin(global_shoulder_angle)]) \
                      * self.arm.upperarm_length * self.scale + shoulder_point
        wrist_point = np.array([math.cos(global_elbow_angle),
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
            angle_start = math.degrees(self.initial_angle + self.arm.angle_constraints[0]['min'])
            angle_extent = math.degrees(self.arm.angle_constraints[0]['max'] - self.arm.angle_constraints[0]['min'])
            self.canvas.draw_arc(shoulder_point[0].tolist(),
                                 shoulder_point[1].tolist(),
                                 25,
                                 start=angle_start,
                                 extent=angle_extent,
                                 outline="white",
                                 fill="gray")

            # Elbow
            angle_start = math.degrees(global_shoulder_angle + self.arm.angle_constraints[1]['min'])
            angle_extent = math.degrees(self.arm.angle_constraints[1]['max'] - self.arm.angle_constraints[1]['min'])
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

        # Draw muscles
        if self.draw_muscles and hasattr(self.muscle, 'A'):
            colors = [int(max(min(signal, 1.), 0.) * 255) for signal in input_signal]

            L = self.arm.upperarm_length / 3. * self.scale # TODO
            angle_offset = [math.pi / 2., -math.pi / 2., math.pi / 2.,
                            -math.pi / 2., math.pi / 2., -math.pi / 2.] # TODO

            for i in range(self.muscle.A.shape[0]):
                point1, point2 = None, None

                # Compute point 1 (shoulder side)
                if self.muscle.A[i][0] == 0.:
                    point1 = np.array([math.cos(global_shoulder_angle), 
                                       math.sin(global_shoulder_angle)]) \
                             * 2*L + shoulder_point # TODO
                else:
                    point1 = np.array([math.cos(self.initial_angle + self.arm.initial_angles[0] + angle_offset[i]), 
                                       math.sin(self.initial_angle + self.arm.initial_angles[0] + angle_offset[i])]) \
                             * self.muscle.A[i][0] * self.scale + shoulder_point

                # Compute point 2 (elbow side)
                if self.muscle.A[i][1] == 0.:
                    point2 = np.array([math.cos(global_shoulder_angle), 
                                       math.sin(global_shoulder_angle)]) \
                             * L + shoulder_point # TODO
                else:
                    point2 = np.array([math.cos(global_elbow_angle + angle_offset[i]), 
                                       math.sin(global_elbow_angle + angle_offset[i])]) \
                             * self.muscle.A[i][1] * self.scale + elbow_point

                # Draw muscle (color is proportional to input_signal)
                self.canvas.draw_line(point1.tolist() + point2.tolist(),
                                      fill='#%02X00%02X' % (colors[i], 255 - colors[i]) ,
                                      width=2)

        # Draw joints
        if self.draw_joints and hasattr(self.muscle, 'A'):
            for i in range(self.muscle.A.shape[0]):
                # Shoulder
                if self.muscle.A[i][0] != 0.:
                    self.canvas.draw_circle(shoulder_point[0].tolist(),
                                            shoulder_point[1].tolist(),
                                            abs(self.muscle.A[i][0]) * self.scale)

                # Elbow
                if self.muscle.A[i][1] != 0.:
                    self.canvas.draw_circle(elbow_point[0].tolist(),
                                            elbow_point[1].tolist(),
                                            abs(self.muscle.A[i][1]) * self.scale)

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
        except tk.TclError:
            pass # to avoid errors when the window is closed


class MathCanvas(tk.Canvas):
    "A canvas where the origin is placed at the bottom left corner."

    def draw_line(self, *args, **kw):
        "TODO : doc..."
        points = np.array(args[0])
        points_array = points.reshape((2, points.shape[0] / 2))
        points_array[:, 1] *= -1
        # TODO : self.canevas_height  self.winfo_height() self.winfo_reqheight()
        points_array[:, 1] += self.winfo_height()
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

