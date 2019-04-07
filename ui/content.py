import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ui.drawingArea import DrawingArea
from ui.env import *
from engine.recognizer import Recognizer

class Content (Gtk.Box):

    def __init__ (self, window):
        Gtk.Box.__init__(self, border_width = 20, valign = Gtk.Align.CENTER, halign = Gtk.Align.CENTER, spacing = 80)
        self.window = window

        # Zone de dessin
        self.drawing_area = DrawingArea(self)

        # Lettre reconnue
        self.recognizer = Recognizer()
        text_label = Gtk.Label('Lettre reconnue:', name = 'text_label')
        self.text_value = Gtk.Label('...', name = 'text_value')

        # Apprendre le bon résultat (mauvais resultat)
        self.learn_entry = Gtk.Entry(max_length = 1, width_chars = 4, max_width_chars = 4, sensitive = False)
        self.learn_button = Gtk.Button(label = 'Apprendre', sensitive = False)
        self.learn_button.connect('clicked', self.learn_button_clicked)

        # Conteneurs
        left_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        left_box.add(self.drawing_area)

        result_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        result_box.add(text_label)
        result_box.add(self.text_value)

        learn_box = Gtk.Box(spacing = 20)
        learn_box.add(self.learn_entry)
        learn_box.add(self.learn_button)

        right_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        right_box.pack_start(result_box, True, False, 0)
        right_box.pack_end(learn_box, True, False, 0)

        self.add(left_box)
        self.add(right_box)

    def recognize_character (self, positions):
        if (len(positions) >= 2):
            res = self.recognizer.recognize(positions)
            self.text_value.set_text(res)
            self.change_buttons_sensitivity(True)

    def learn_button_clicked (self, obj = None, data = None):
        text = self.learn_entry.get_text().upper()
        if (len(text) == 1):
            self.learn_entry.set_text('')
            self.recognizer.learn_from_positions(text)
            self.text_value.set_text(text)
            self.change_buttons_sensitivity(False)

    def change_buttons_sensitivity (self, sensitive):
        self.learn_entry.set_sensitive(sensitive)
        self.learn_button.set_sensitive(sensitive)
