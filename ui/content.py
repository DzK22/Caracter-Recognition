import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ui.drawingArea import DrawingArea
from ui.env import *
from engine.recognizer import Recognizer
from engine.letter import Letter
from engine.symbol import Symbol

class Content (Gtk.Box):

    def __init__ (self, window):
        Gtk.Box.__init__(self, border_width = 20, valign = Gtk.Align.CENTER,
                         halign = Gtk.Align.CENTER, spacing = 80)
        self.window = window

        # Drawing area
        self.drawing_area = DrawingArea(self)

        # Letter / Symbols switcher
        self.__type = 'letter';
        self.__type_letter_button = Gtk.ToggleButton('Lettre', active = True)
        self.__type_symbol_button = Gtk.ToggleButton('Symbole')
        self.__type_letter_button_handler = self.__type_letter_button.connect(
                                                'clicked', self.__change_type)
        self.__type_symbol_button_handler = self.__type_symbol_button.connect(
                                                'clicked', self.__change_type)

        # Recognized character
        self.recognizer = Recognizer(self.__type)
        text_label = Gtk.Label('Caractère reconnu:', name = 'text_label')
        self.text_label = Gtk.Label('...', name = 'text_value_label', width_chars = 10)

        # Learn the good result
        self.__learn_entry = Gtk.Entry(max_length = 10, width_chars = 10,
                                       sensitive = False)
        self.__learn_button = Gtk.Button(label = 'Apprendre', sensitive = False)
        self.__learn_entry.connect('changed', self.__learn_entry_changed)
        self.__learn_button.connect('clicked', self.__learn_button_clicked)

        # Containers
        left_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        left_box.add(self.drawing_area)

        type_switcher = Gtk.StackSwitcher()
        type_switcher.add(self.__type_letter_button)
        type_switcher.add(self.__type_symbol_button)
        result_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                             spacing = 10)
        result_box.add(text_label)
        result_box.add(self.text_label)

        learn_box = Gtk.Box(spacing = 20, halign = Gtk.Align.CENTER)
        learn_box.add(self.__learn_entry)
        learn_box.add(self.__learn_button)

        right_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        right_box.pack_start(type_switcher, True, False, 0)
        right_box.add(result_box)
        right_box.pack_end(learn_box, True, False, 0)

        self.add(left_box)
        self.add(right_box)

    def recognize_character (self, positions):
        """ Start the recognition of a draw (with positions) """
        if len(positions) >= 2:
            res = self.recognizer.recognize(positions)
            self.text_label.set_text(res)
            self.change_buttons_sensitivity(True)

    def change_buttons_sensitivity (self, sensitive):
        """ Make sensitive or not the learn button and entry """
        self.__learn_entry.set_sensitive(sensitive)
        self.__learn_button.set_sensitive(sensitive)
        self.__learn_entry_changed(self.__learn_entry)

    def __learn_button_clicked (self, obj = None, data = None):
        """ To save the good character for the current recognizer positions """
        text = self.__learn_entry.get_text().upper()
        self.__learn_entry.set_text('')
        self.recognizer.learn_from_positions(text)
        self.text_label.set_text(text)
        if len(self.drawing_area.positions) > 0:
            self.change_buttons_sensitivity(False)

    def __change_type (self, obj, data = None):
        """ Change the recognition type (letter / symbol). Letter = [A-Z] and
            Symbol = [0-9], space, return, shift, caps lock, back-space """
        if obj is self.__type_letter_button:
            obj_handler = self.__type_letter_button_handler
            obj_val = 'letter'
            other = self.__type_symbol_button
            other_handler = self.__type_symbol_button_handler
        else:
            obj_handler = self.__type_symbol_button_handler
            obj_val = 'symbol'
            other = self.__type_letter_button
            other_handler = self.__type_letter_button_handler

        if obj.get_active():
            self.__type = obj_val
            self.recognizer.change_type(self.__type)
            self.recognize_character(self.drawing_area.positions)
            with other.handler_block(other_handler):
                other.set_active(False)
        else:
            with obj.handler_block(obj_handler):
                obj.set_active(True)

    def __learn_entry_changed (self, obj, data = None):
        """ On entry input, check if the text can be a valid character """
        if self.__type == 'letter':
            car = Letter(obj.get_text().upper())
        else:
            car = Symbol(obj.get_text())

        if (self.__learn_button.get_sensitive() is False) and \
        (car.val is not None):
            self.__learn_button.set_sensitive(True)
        elif (self.__learn_button.get_sensitive() is True) and \
        (car.val is None):
            self.__learn_button.set_sensitive(False)
