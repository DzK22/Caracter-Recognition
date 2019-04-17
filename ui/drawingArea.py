import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, cairo
from ui.env import *
import math

class DrawingArea (Gtk.DrawingArea):

    def __init__ (self, window_content):
        Gtk.DrawingArea.__init__(self,
            width_request = DRAWING_AREA_SIZE,
            height_request = DRAWING_AREA_SIZE,
            name = 'drawing_area')
        self.__window_content = window_content;
        self.positions = []
        self.__button_pressed = False

        self.connect('draw', self.__draw_event)
        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK |
                        Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.connect('button-press-event', self.__button_press_event)
        self.connect('button-release-event', self.__button_release_event)
        self.connect('motion-notify-event', self.__motion_notify_event)

    def clear (self, obj = None):
        """ Clear all the drawing from the drawing area and the array """
        self.positions.clear()
        self.queue_draw()
        self.__window_content.text_label.set_text('...')
        self.__window_content.change_buttons_sensitivity(False)

    def __button_press_event (self, obj = None, event = None):
        """ The mouse button has been pressed """
        self.__button_pressed = True

    def __button_release_event (self, obj = None, event = None):
        """ The mouse button has been released, append position (None, None) """
        self.__button_pressed = False
        self.positions.append((None, None))
        if self.positions.count((None, None)) < len(self.positions):
            self.__window_content.recognize_character(self.positions)

    def __motion_notify_event (self, obj, event):
        """ The cursor position have changed over the drawing area, add the new
            position if the mouse button is pressed """
        x, y = int(event.x), int(event.y)

        if (self.__button_pressed is True) and (x in range(0, \
            DRAWING_AREA_SIZE)) and (y in range(0, DRAWING_AREA_SIZE)):
            self.positions.append((x, y))
            self.queue_draw()

    def __draw_event (self, obj, ctx):
        """ Called when the widget receive a draw signal, show all the points
            of the draw """
        ctx.set_source_rgba(0, 0, 0, 0.2)
        ctx.rectangle(0, 0, DRAWING_AREA_SIZE, DRAWING_AREA_SIZE)
        ctx.fill()

        font_color = self.get_style_context().get_color(Gtk.StateFlags.NORMAL)
        font_color.parse('rgb')
        ctx.set_source_rgb(font_color.red, font_color.green, font_color.blue)
        ctx.set_line_width(6)
        old_pos = None, None

        for (x, y) in self.positions:
            if old_pos != (None, None):
                ctx.move_to(old_pos[0], old_pos[1])

            if (x, y) != (None, None):
                ctx.line_to(x, y)
                ctx.stroke()
            else:
                ctx.new_path()

            old_pos = (x, y)
