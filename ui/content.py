import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

DRAWING_AREA_WIDTH = 100
DRAWING_AREA_HEIGHT = 100

class Content (Gtk.Box):

    def __init__ (self, window):

        Gtk.Box.__init__(self)
        self.window = window

        # Zone de dessin
        self.drawing_area = Gtk.DrawingArea(
            width_request = DRAWING_AREA_WIDTH,
            height_request = DRAWING_AREA_HEIGHT)
        self.drawing_area.connect('draw', self.drawing_event)

        # Conteneurs
        left_vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        drawing_area_box = Gtk.Box(name = 'drawing_area_box')
        drawing_area_box.add(self.drawing_area)
        left_vbox.add(drawing_area_box)

        right_vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.add(left_vbox)
        self.add(right_vbox)
        self.show_all()

    def drawing_event (self, obj):
        self.queue_draw()

    def clear (self, obj):
        pass
