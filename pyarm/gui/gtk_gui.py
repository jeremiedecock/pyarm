# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from pyarm.gui.abstract_gui import AbstractGUI
import numpy as np
import math
import time
import pygtk
pygtk.require('2.0')
import gtk

class GUI(AbstractGUI):
    "Tkinter graphical user interface."

    running = None

    arm = None
    muscle = None

    window = None
    drawable = None
    gtk_gc = None

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
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('pyarm')
        self.window.connect('destroy', self.quit_handler)

        # Organize widgets in a vertical box
        vbox = gtk.VBox()
        self.window.add(vbox)

        # Shoulder labels

        # Elbow labels

        # Canvas
        drawing_area = gtk.DrawingArea()
        drawing_area.set_size_request(self.canevas_width, self.canevas_height)
        vbox.pack_start(drawing_area)

        # Button
        quit_button = gtk.Button("Quit")
        quit_button.connect("clicked", self.quit_handler)
        vbox.pack_start(quit_button)
        
        # Show all
        self.window.show_all()

        # Make drawable and graphics_context
        self.drawable = drawing_area.window
        self.gtk_gc = self.drawable.new_gc()

        # Run
        self.running = True


    def quit_handler(self, widget) :
        " Quit the application."
        self.running = False
        gtk.main_quit()


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

        ## Generate an expose event (could just draw here as well).
        #self.queue_draw()

        ###self.gtk_gc.set_rgb_fg_color(gtk.gdk.color_parse("yellow"))
        ###self.drawable.draw_arc(self.gtk_gc, True, 200, 100, 200, 200, 0, 360*64)
        ###self.gtk_gc.set_rgb_fg_color(gtk.gdk.Color(0, 0, 0))             # black
        ###self.drawable.draw_arc(self.gtk_gc, True, 240, 145, 30, 40, 0, 360*64)
        ###self.drawable.draw_arc(self.gtk_gc, True, 330, 145, 30, 40, 0, 360*64)
        ###self.gtk_gc.line_width = 6
        ###self.drawable.draw_arc(self.gtk_gc, False, 240, 150, 120, 110, 200*64, 140*64)

        #try:
        #    # Update labels
        #    self.label_strings['shoulder_angle'].set("angle = %1.2frd (%03d°)" \
        #        % (self.arm.angles[0], math.degrees(self.arm.angles[0])))
        #    self.label_strings['shoulder_velocity'].set("velocity = %1.2frd/s" \
        #        % self.arm.velocities[0])
        #    self.label_strings['shoulder_torque'].set("torque = %03dN.m" \
        #        % torque[0])
        #    self.label_strings['elbow_angle'].set("angle = %1.2frd (%03d°)" \
        #        % (self.arm.angles[1], math.degrees(self.arm.angles[1])))
        #    self.label_strings['elbow_velocity'].set("velocity = %1.2frd/s" \
        #        % self.arm.velocities[1])
        #    self.label_strings['elbow_torque'].set("torque = %03dN.m" \
        #        % torque[1])

        # Update the caneva
        self.draw_shapes(input_signal)

        # Process all pending events.
        while gtk.events_pending():
            gtk.main_iteration(False)
            
        self.take_a_screenshot()
        #except tk.TclError:
        #    pass # to avoid errors when the window is closed

    def take_a_screenshot(self):
        "Take a screenshot and save it into a file."
        #w = gtk.gdk.get_default_root_window()
        #sz = w.get_size()
        #print "The size of the window is %d x %d" % sz
        #pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
        #pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
        #if (pb != None):
        #    pb.save("screenshot.png","png")
        #    print "Screenshot saved to screenshot.png."
        #else:
        #    print "Unable to get the screenshot."


        # Either "png" or "jpeg"
        format = "png"

        screenshot = gtk.gdk.Pixbuf.get_from_drawable(
                     gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, self.canevas_width, self.canevas_height),
                     self.drawable,
                     gtk.gdk.colormap_get_system(),
                     0, 0, 0, 0, self.canevas_width, self.canevas_height)

        # Pixbuf's have a save method 
        # Note that png doesnt support the quality argument. 
        screenshot.save("screenshot_" + str(time.time()) + "." + format, format)

        ### To avoid a big memory leak
        ##del screenshot
        ##gc.collect()

    def clear_canvas(self):
        "Clear the canvas"
        self.gtk_gc.set_rgb_fg_color(gtk.gdk.color_parse("white"))

        # Draw white background
        self.drawable.draw_rectangle(self.gtk_gc,
                                     True,
                                     0, 0,
                                     self.canevas_width, self.canevas_height)

    def draw_line(self, *args, **kw):
        "TODO : doc..."
        points = args[0]
        points = [(int(points[i-1]), int(-points[i] + self.canevas_height)) \
                 for i in range(len(points))[1::2]]

        self.gtk_gc.set_rgb_fg_color(gtk.gdk.color_parse("black"))
        self.drawable.draw_lines(self.gtk_gc, points)

    def draw_arc(self, x_point, y_point, radius, **kw):
        "TODO : doc..."
        #radius = abs(radius)
        #y_point *= -1
        #y_point += self.canvas.winfo_height() # TODO
        #args = (x_point + radius,
        #        y_point + radius,
        #        x_point - radius,
        #        y_point - radius)
        #return self.canvas.create_arc(args, kw)

    def draw_circle(self, x_point, y_point, radius, **kw):
        "TODO : doc..."
        radius = abs(radius)
        y_point = -y_point + self.canevas_height

        self.gtk_gc.set_rgb_fg_color(gtk.gdk.color_parse("black"))
        self.drawable.draw_arc(self.gtk_gc,
                               False,
                               x_point - radius, y_point - radius,
                               2 * radius, 2 * radius,
                               0, 360*64)

    def draw_text(self, x_point, y_point, **kw):
        "TODO : doc..."
        #y_point *= -1
        #y_point += self.canvas.winfo_height() # TODO
        #args = (x_point, y_point)
        #return self.canvas.create_text(args, kw)
        pass

