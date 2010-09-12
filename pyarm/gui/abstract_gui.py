# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import math

class AbstractGUI:

    arm = None
    muscle = None

    initial_angle = 0.

    canevas_width = 800
    canevas_height = 600
    scale = 450. # px/m (pixels per meter)

    draw_angles_bounds = False
    draw_angles = False
    draw_muscles = False
    draw_joints = False

    def __init__(self):
        raise NotImplementedError()

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
        self.clear_canvas()

        # Draw angles bounds
        if self.draw_angles_bounds:
            # Shoulder
            angle_start = math.degrees(self.initial_angle + self.arm.angle_constraints[0]['min'])
            angle_extent = math.degrees(self.arm.angle_constraints[0]['max'] - self.arm.angle_constraints[0]['min'])
            self.draw_arc(shoulder_point[0].tolist(),
                          shoulder_point[1].tolist(),
                          25,
                          start=angle_start,
                          extent=angle_extent,
                          outline="white",
                          fill="gray")

            # Elbow
            angle_start = math.degrees(global_shoulder_angle + self.arm.angle_constraints[1]['min'])
            angle_extent = math.degrees(self.arm.angle_constraints[1]['max'] - self.arm.angle_constraints[1]['min'])
            self.draw_arc(elbow_point[0].tolist(),
                          elbow_point[1].tolist(),
                          25,
                          start=angle_start,
                          extent=angle_extent,
                          outline="white",
                          fill="gray")

        # Draw angles
        if self.draw_angles:
            # Shoulder arc angle
            self.draw_arc(shoulder_point[0].tolist(),
                          shoulder_point[1].tolist(),
                          25,
                          start=math.degrees(self.initial_angle),
                          extent=math.degrees(shoulder_angle))

            # Elbow arc angle
            self.draw_arc(elbow_point[0].tolist(),
                          elbow_point[1].tolist(),
                          25,
                          start=math.degrees(global_shoulder_angle),
                          extent=math.degrees(elbow_angle))

            # Shoulder initial line
            point1 = shoulder_point
            point2 = np.array([math.cos(self.initial_angle), 
                               math.sin(self.initial_angle)]) \
                     * 30 + shoulder_point
            self.draw_line(point1.tolist() + point2.tolist(),
                                    width=1)

            # Elbow initial line
            point1 = elbow_point
            point2 = np.array([math.cos(global_shoulder_angle), 
                               math.sin(global_shoulder_angle)]) \
                     * 30 + elbow_point
            self.draw_line(point1.tolist() + point2.tolist(),
                                  width=1)

        # Draw limbs
        self.draw_line(shoulder_point.tolist() + elbow_point.tolist(),
                              fill="black",
                              width=5)
        self.draw_line(elbow_point.tolist() + wrist_point.tolist(),
                              fill="black",
                              width=5)

        # Draw muscles
        if self.draw_muscles and hasattr(self.muscle, 'A'):
            colors = [int(max(min(signal, 1.), 0.) * 255) for signal in input_signal]

            L = self.arm.upperarm_length / 3. * self.scale # TODO
            # TODO : remove the if statement above
            if self.muscle.name == 'Kambara':
                angle_offset = [0., 0., 0.,
                                0., 0., 0.] # TODO
            else:
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
                self.draw_line(point1.tolist() + point2.tolist(),
                                      fill='#%02X00%02X' % (colors[i], 255 - colors[i]) ,
                                      width=2)

        # Draw joints
        if self.draw_joints and hasattr(self.muscle, 'A'):
            for i in range(self.muscle.A.shape[0]):
                # Shoulder
                if self.muscle.A[i][0] != 0.:
                    self.draw_circle(shoulder_point[0].tolist(),
                                            shoulder_point[1].tolist(),
                                            abs(self.muscle.A[i][0]) * self.scale)

                # Elbow
                if self.muscle.A[i][1] != 0.:
                    self.draw_circle(elbow_point[0].tolist(),
                                            elbow_point[1].tolist(),
                                            abs(self.muscle.A[i][1]) * self.scale)

    def update(self, input_signal, torque, acceleration):
        "Redraw the screen."
        raise NotImplementedError()

    def clear_canvas(self):
        "Clear the canvas."
        raise NotImplementedError()

    def draw_line(self, *args, **kw):
        "Draw a line on the canvas."
        raise NotImplementedError()

    def draw_arc(self, x_point, y_point, radius, **kw):
        "Draw an arc on the canvas."
        raise NotImplementedError()

    def draw_circle(self, x_point, y_point, radius, **kw):
        "Draw a circle on the canvas."
        raise NotImplementedError()

    def draw_text(self, x_point, y_point, **kw):
        "Print text on the canvas."
        raise NotImplementedError()

