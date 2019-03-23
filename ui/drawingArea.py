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

        self.window_content = window_content;
        self.cursor_positions = []
        self.button_pressed = False

        self.connect('draw', self.draw_event)
        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.connect('button-press-event', self.button_press_event)
        self.connect('button-release-event', self.button_release_event)
        self.connect('motion-notify-event', self.motion_notify_event)

    def clear (self, obj = None):
        self.cursor_positions.clear()
        self.queue_draw()
        self.window_content.text_value.set_text('...')

    def button_press_event (self, obj = None, event = None):
        self.button_pressed = True

    def button_release_event (self, obj = None, event = None):
        self.button_pressed = False
        self.cursor_positions.append((None, None))
        self.window_content.recognize_letter(self.cursor_positions)

    def motion_notify_event (self, obj, event):
        x, y = int(event.x), int(event.y)

        if ((self.button_pressed is True) and
        (x in range(0, DRAWING_AREA_SIZE)) and
        (y in range(0, DRAWING_AREA_SIZE))):
            self.cursor_positions.append((x, y))
            self.queue_draw()

    def draw_event (self, obj, ctx):
        ctx.set_source_rgba(0, 0, 0, 0.2)
        ctx.rectangle(0, 0, DRAWING_AREA_SIZE, DRAWING_AREA_SIZE)
        ctx.fill()

        font_color = self.get_style_context().get_color(Gtk.StateFlags.NORMAL)
        font_color.parse('rgb')
        ctx.set_source_rgb(font_color.red, font_color.green, font_color.blue)
        ctx.set_line_width(6)
        old_pos = None, None

        for (x, y) in self.cursor_positions:
            if (old_pos != (None, None)):
                ctx.move_to(old_pos[0], old_pos[1])

            if ((x, y) != (None, None)):
                ctx.line_to(x, y)
                ctx.stroke()
            else:
                ctx.new_path()

            old_pos = (x, y)
