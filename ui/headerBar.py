import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ui.env import *

class HeaderBar (Gtk.HeaderBar):

    def __init__ (self, window):
        Gtk.HeaderBar.__init__(self,
            show_close_button = True,
            title = PROGRAM_NAME)
        self.__window = window

        # bouton effacer
        clear_button = Gtk.Button('Effacer', name = 'clear_button')
        clear_button.connect('clicked', \
            self.__window.content.drawing_area.clear)
        self.pack_start(clear_button)

        # bouton menu
        menu_button = Gtk.Button.new_from_icon_name(
            'open-menu-symbolic',
            Gtk.IconSize.MENU)
        menu_button.connect('clicked', self.__show_menu)
        self.pack_end(menu_button)

    def __show_menu (self, obj):
        popover = Gtk.Popover(relative_to = obj)
        popover_box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            border_width = 6)

        reset_button = Gtk.ModelButton('Remmetre à zero', xalign = 0)
        reset_button.connect('clicked', self.__reset_positions)
        about_button = Gtk.ModelButton('À propos', xalign = 0)
        about_button.connect('clicked', self.__show_about_dialog)
        quit_button = Gtk.ModelButton('Quitter', xalign = 0)
        quit_button.connect('clicked', Gtk.main_quit)

        popover_box.add(reset_button)
        popover_box.add(about_button)
        popover_box.add(quit_button)
        popover.add(popover_box)
        popover_box.show_all()
        popover.popup()

    def __show_about_dialog (self, obj = None):
        dialog = Gtk.AboutDialog(
            authors = ['François Grabenstaetter', 'Danyl El-Kabir'],
            license_type = Gtk.License.GPL_3_0,
            version = VERSION,
            modal = True,
            transient_for = self.__window,
            logo_icon_name = 'system-search-symbolic',
            comments = 'Un utilitaire de reconnaissance de caractère pour le '
                'projet de POO2')
        dialog.show()

    def __reset_positions (self, obj = None):
        self.__window.content.recognizer.reset_all_positions()
