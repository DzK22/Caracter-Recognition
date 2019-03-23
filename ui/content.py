import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ui.drawingArea import DrawingArea
from ui.env import *
from engine.letterRecognizer import LetterRecognizer

class Content (Gtk.Box):

    def __init__ (self, window):
        Gtk.Box.__init__(self, border_width = 20, valign = Gtk.Align.CENTER, halign = Gtk.Align.CENTER, spacing = 80)
        self.window = window

        # Zone de dessin
        self.drawing_area = DrawingArea(self)

        # Lettre reconnue
        self.letter_recognizer = LetterRecognizer()
        text_label = Gtk.Label('Lettre reconnue:', name = 'text_label')
        self.text_value = Gtk.Label('...', name = 'text_value')

        # Conteneurs
        left_vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        left_vbox.add(self.drawing_area)

        right_vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        right_vbox.add(text_label)
        right_vbox.add(self.text_value)

        self.add(left_vbox)
        self.add(right_vbox)

    def recognize_letter (self, cursor_positions):
        if (len(cursor_positions) >= 2):
            self.letter_recognizer.calculate(cursor_positions)
            self.text_value.set_text(self.letter_recognizer.letter)
