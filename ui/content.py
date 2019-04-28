import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ui.drawingArea import DrawingArea
from ui.env import *
from engine.recognizer import Recognizer
from engine.letter import Letter
from engine.symbol import Symbol
from engine.punctuation import Punctuation
from engine.extended import Extended
from engine.accent import Accent

class Content (Gtk.Box):

    def __init__ (self, window):
        Gtk.Box.__init__(self, border_width = 20, valign = Gtk.Align.CENTER,
                         halign = Gtk.Align.CENTER, spacing = 80)
        self.window = window

        # Drawing area
        self.drawing_area = DrawingArea(self)

        # Letter / Symbols switcher
        self.__type = 'letter';
        self.__type_label = Gtk.Label('Type:', name = 'type_label')
        self.__type_button = Gtk.Button('Lettre', width_request = 160,
                                        name = 'type_button');
        self.__type_button.connect('clicked', self.__change_type)

        # Recognized character
        self.recognizer = Recognizer(self.__type)
        text_label = Gtk.Label('Caractère reconnu:', name = 'text_label')
        self.text_label = Gtk.Label('...', name = 'text_value_label',
                                    width_chars = 10)

        # Learn the good result
        self.__learn_character = Gtk.Button(label = '☝',
                                            name = 'learn_character',
                                            sensitive = False)
        self.__learn_character.connect('clicked',
                                       self.__learn_character_clicked)
        self.__learn_button = Gtk.Button(label = 'Apprendre', sensitive = False)
        self.__learn_button.connect('clicked', self.__learn_button_clicked)

        # Containers
        left_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        left_box.add(self.drawing_area)

        type_switcher = Gtk.Box(spacing = 20, halign = Gtk.Align.CENTER)
        type_switcher.add(self.__type_label)
        type_switcher.add(self.__type_button)
        result_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                             spacing = 10)
        result_box.add(text_label)
        result_box.add(self.text_label)

        learn_box = Gtk.Box(spacing = 20, halign = Gtk.Align.CENTER)
        learn_box.add(self.__learn_character)
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

    def clear (self, obj = None, data = None):
        """ Clear the drawing area """
        self.__learn_character.set_label('☝')
        self.drawing_area.clear()

    def __change_type (self, obj, data = None):
        """ Change the recognition type (letter / symbol / punctuation /
            extended / accent). """
        types = ('letter', 'symbol', 'punctuation', 'extended', 'accent')
        types_name = ('Lettre', 'Symbole', 'Ponctuation', 'Étendu', 'Accent')
        popover = Gtk.Popover().new(self.__type_button)
        popover.set_position(Gtk.PositionType.BOTTOM)
        popover.set_size_request(150, -1)
        popover_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                              border_width = 6)

        def button_click_event (obj, data = None):
            self.__type = types[types_name.index(obj.get_label())]
            self.__type_button.set_label(obj.get_label())
            self.recognizer.change_type(self.__type)
            self.recognize_character(self.drawing_area.positions)
            self.__learn_character.set_label('☝')

        for key, type in enumerate(types):
            if type == self.__type:
                continue
            button = Gtk.ModelButton(types_name[key], xalign = 0)
            button.connect('clicked', button_click_event)
            popover_box.add(button)
        popover_box.show_all()
        popover.add(popover_box)
        popover.popup()

    def change_buttons_sensitivity (self, sensitive):
        """ Make sensitive or not the learn button and entry """
        self.__learn_character.set_sensitive(sensitive)
        if sensitive and (self.__learn_character.get_label() == '☝'):
            self.__learn_button.set_sensitive(False)
        else:
            self.__learn_button.set_sensitive(sensitive)

    def __learn_button_clicked (self, obj = None, data = None):
        """ To save the good character for the current recognizer positions """
        text = self.__learn_character.get_label()
        self.__learn_character.set_label('☝')
        self.recognizer.learn_from_positions(text)
        self.text_label.set_text(text)
        if len(self.drawing_area.positions) > 0:
            self.change_buttons_sensitivity(False)

    def __learn_character_clicked (self, obj, data = None):
        """ On click event, show a popover with all available characters """
        popover = Gtk.Popover().new(self.__learn_character)
        popover_box = Gtk.FlowBox(min_children_per_line = 6,
                                  max_children_per_line = 6,
                                  selection_mode = Gtk.SelectionMode.NONE)
        popover.add(popover_box)

        def button_click_event (obj, data = None):
            if self.__learn_button.get_sensitive() is False:
                self.__learn_button.set_sensitive(True)
            self.__learn_character.set_label(obj.get_label())

        for char in self.recognizer.valid_characters:
            if char.val != self.__learn_character.get_label():
                button = Gtk.ModelButton(char.val)
                button.connect('clicked', button_click_event)
                popover_box.add(button)

        popover_box.show_all()
        popover.popup()
