import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ui.drawingArea import DrawingArea
from ui.env import *

class Content (Gtk.Box):

    def __init__ (self, window):

        Gtk.Box.__init__(self, border_width = 20, valign = Gtk.Align.CENTER, halign = Gtk.Align.CENTER, spacing = 80)
        self.window = window

        # Zone de dessin
        self.drawing_area = DrawingArea()

        # Lettre reconnue
        text_label = Gtk.Label('Lettre reconnue:', name = 'text_label')
        self.text_value = Gtk.Label(name = 'text_value')

        # Conteneurs
        left_vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        left_vbox.add(self.drawing_area)

        right_vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        right_vbox.add(text_label)
        right_vbox.add(self.text_value)

        self.add(left_vbox)
        self.add(right_vbox)
