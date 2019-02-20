import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, cairo
from ui.env import *
import math

class DrawingArea (Gtk.DrawingArea):

    def __init__ (self):

        Gtk.DrawingArea.__init__(self,
            width_request = DRAWING_AREA_WIDTH,
            height_request = DRAWING_AREA_HEIGHT,
            name = 'drawing_area')

        self.cursor_positions = []
        self.button_pressed = False

        self.connect('draw', self.draw_event)
        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.connect('button-press-event', self.button_press_event)
        self.connect('button-release-event', self.button_release_event)
        self.connect('motion-notify-event', self.motion_notify_event)

    def button_press_event (self, obj = None, event = None):

        self.cursor_positions.clear()
        self.button_pressed = True

    def button_release_event (self, obj = None, event = None):

        self.button_pressed = False

    def motion_notify_event (self, obj, event):

        x, y = int(event.x), int(event.y)

        if ((self.button_pressed is True) and
        (x in range(0, DRAWING_AREA_WIDTH)) and
        (y in range(0, DRAWING_AREA_HEIGHT))):
            self.cursor_positions.append((x, y))
            self.queue_draw()

    def draw_event (self, obj, ctx):

        ctx.set_source_rgba(0, 0, 0, 0.2)
        ctx.rectangle(0, 0, DRAWING_AREA_WIDTH, DRAWING_AREA_HEIGHT)
        ctx.fill()

        font_color = self.get_style_context().get_color(Gtk.StateFlags.NORMAL)
        font_color.parse('rgb')
        ctx.set_source_rgb(font_color.red, font_color.green, font_color.blue)
        ctx.set_line_width(6)
        old_pos = None

        for (x, y) in self.cursor_positions:
            if (old_pos is not None):
                ctx.move_to(old_pos[0], old_pos[1])
                ctx.line_to(x, y)
                ctx.stroke()
            old_pos = (x, y)
