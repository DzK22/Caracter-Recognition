import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
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
            self.__window.content.clear)
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

        reset_button = Gtk.ModelButton('Remmetre par défaut', xalign = 0)
        reset_button.connect('clicked', self.__show_reset_default_dialog)
        graffiti_button = Gtk.ModelButton('Dessins Graffiti', xalign = 0)
        graffiti_button.connect('clicked', self.__show_graffiti_dialog)
        about_button = Gtk.ModelButton('À propos', xalign = 0)
        about_button.connect('clicked', self.__show_about_dialog)
        quit_button = Gtk.ModelButton('Quitter', xalign = 0)
        quit_button.connect('clicked', Gtk.main_quit)

        popover_box.add(reset_button)
        popover_box.add(graffiti_button)
        popover_box.add(about_button)
        popover_box.add(quit_button)
        popover.add(popover_box)
        popover_box.show_all()
        popover.popup()

    def __show_reset_default_dialog (self, obj = None):
        dialog = Gtk.MessageDialog(
            modal = True,
            transient_for = self.__window,
            text = '<b>Remettre l\'apprentissage des caractères par défaut ?</b>',
            use_markup = True,
            secondary_text = 'Les caractères courrants seront effacés',
            buttons = Gtk.ButtonsType.OK_CANCEL,
            message_type = Gtk.MessageType.QUESTION
        )

        def cancel (obj = None):
            dialog.close()

        def valid (obj = None):
            self.__window.content.recognizer.reset_default_all_positions()
            dialog.close()

        cancel_button = dialog.get_widget_for_response(Gtk.ResponseType.CANCEL)
        cancel_button.connect('clicked', cancel)
        confirm_button = dialog.get_widget_for_response(Gtk.ResponseType.OK)
        confirm_button.connect('clicked', valid)
        dialog.show();

    def __show_graffiti_dialog (self, obj = None):
        dialog = Gtk.Window(
            modal = True,
            transient_for = self.__window,
            resizable = False
        )
        dialog_headerbar = Gtk.HeaderBar(show_close_button = True,
                                         title = "Dessins Graffiti")
        dialog.set_titlebar(dialog_headerbar)
        dialog.add_events(Gdk.EventMask.KEY_PRESS_MASK)

        def dialog_key_press (obj, event):
            if event.hardware_keycode == 9:
                dialog.close()
        dialog.connect('key_press_event', dialog_key_press)

        img = Gtk.Image.new_from_file('img/graffiti_vertical.png')
        img_width = img.get_pixbuf().get_width()
        win_height = self.__window.get_size()[1]
        scrolled_window = Gtk.ScrolledWindow(
            min_content_width = img_width,
            max_content_width = img_width,
            min_content_height = win_height,
            max_content_height = win_height
        )

        scrolled_window.add(img)
        dialog.add(scrolled_window)
        dialog.show_all()

    def __show_about_dialog (self, obj = None):
        dialog = Gtk.AboutDialog(
            authors = ['François Grabenstaetter', 'Danyl El-Kabir'],
            license_type = Gtk.License.GPL_3_0,
            version = VERSION,
            modal = True,
            transient_for = self.__window,
            logo_icon_name = 'system-search-symbolic',
            comments = 'Un utilitaire de reconnaissance de caractère pour le '
                'projet de POO2'
        )
        dialog.show()
