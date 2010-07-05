# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from PySFML import sf
import math
import time
import fig
import warnings

class GUI:
    "SFML graphical user interface."

    # The state of the arm is updated at every tick_duration time (s)
    delta_time  = 0.01
    former_time = 0.
    init_time = 0.

    realtime = True
    screencast = None

    agent = None
    arm = None
    muscle = None

    window = None
    background_color = None
    foreground_color = None
    text1 = None
    text2 = None
    line1 = None
    line2 = None
    LENGTH_SCALE = 300. # px/m (pixels per meter)

    def __init__(self, muscle, arm, agent=None, realtime=False,
                 screencast=False):
        self.arm = arm
        self.muscle = muscle
        self.agent = agent

        # Create the main window
        self.window = sf.RenderWindow(sf.VideoMode(800, 600),
                                      'pyArm (' + muscle.name + ' - ' + arm.name + ')')

        self.background_color = sf.Color(255, 255, 255, 255)
        self.foreground_color = sf.Color(0, 0, 0, 255)

        self.text1 = sf.String("", Size=16)
        self.text1.SetColor(self.foreground_color)
        self.text1.SetPosition(20, 10)

        self.text2 = sf.String("", Size=16)
        self.text2.SetColor(self.foreground_color)
        self.text2.SetPosition(20, 40)

        self.line1 = sf.Shape.Line(0, 0, 0,
                                   self.arm.upperarm_length * self.LENGTH_SCALE,
                                   10, self.background_color, 2,
                                   self.foreground_color)
        self.centerLine(self.line1)

        self.line2 = sf.Shape.Line(0, 0, 0,
                                   self.arm.forearm_length * self.LENGTH_SCALE,
                                   10, self.background_color, 2,
                                   self.foreground_color)
        self.centerLine(self.line2)

        self.realtime = realtime
        self.screencast = screencast
        
        if screencast:
            warnings.warn("screencast option is not yet implemented for SFML gui.")

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

    def centerLine(self, line):
        screen_center = (self.window.GetWidth() / 2,
                         self.window.GetHeight() / 2)
        line.SetPosition(*screen_center)

    def translateLine(self, line, line_ref):
        p0   = line_ref.TransformToGlobal(*line_ref.GetPointPosition(0))
        p1   = line_ref.TransformToGlobal(*line_ref.GetPointPosition(1))
        vect = (p1[0]-p0[0] , p1[1]-p0[1])

        line.Move(*vect)

    def updateShapes(self):
        # Line 1
        self.line1.SetRotation(math.degrees(self.arm.angles[0]))

        # Line 2
        self.centerLine(self.line2)
        self.line2.SetRotation(math.degrees(self.arm.angles[0]))
        self.line2.Rotate(math.degrees(self.arm.angles[1]))
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

            key_input = (window_input.IsKeyDown(sf.Key.Numpad1),
                         window_input.IsKeyDown(sf.Key.Numpad2),
                         window_input.IsKeyDown(sf.Key.Numpad3),
                         window_input.IsKeyDown(sf.Key.Numpad4),
                         window_input.IsKeyDown(sf.Key.Numpad5),
                         window_input.IsKeyDown(sf.Key.Numpad6))

            # Compute delta time
            current_time = time.time()

            if self.realtime:
                self.delta_time = current_time - self.former_time

            fig.append('dtime', self.delta_time)

            elapsed_time = current_time - self.init_time

            # Get input signals
            input_signal = None
            if self.agent == None:
                input_signal = [float(flag) for flag in key_input]
            else:
                input_signal = self.agent.get_action(velocities=self.arm.velocities,
                                                     angles=self.arm.angles,
                                                     time=elapsed_time)
        
            fig.append('input signal', input_signal)

            # Update angles (physics)
            torque = self.muscle.update(input_signal,
                                        self.arm.angles,
                                        self.delta_time)
            acceleration = self.arm.update(torque, self.delta_time)

            # Update clock
            self.former_time = current_time

            # Update the window
            self.updateShapes()
            self.text1.SetText("Shoulder : angle = %1.2frd (%03d°)   velocity = %1.2frd/s   torque = %03dN.m" % (self.arm.angles[0], math.degrees(self.arm.angles[0]), self.arm.velocities[0], torque[0]))
            self.text2.SetText("Elbow    : angle = %1.2frd (%03d°)   velocity = %1.2frd/s   torque = %03dN.m" % (self.arm.angles[1], math.degrees(self.arm.angles[1]), self.arm.velocities[1], torque[1]))

            self.window.Clear(self.background_color)

            self.window.Draw(self.text1)
            self.window.Draw(self.text2)
            self.window.Draw(self.line1)
            self.window.Draw(self.line2)

            self.window.Display()

