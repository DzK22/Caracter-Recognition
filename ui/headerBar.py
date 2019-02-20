import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

VERSION = '0.0'

class HeaderBar (Gtk.HeaderBar):

    def __init__ (self, window):

        Gtk.HeaderBar.__init__(self,
            show_close_button = True,
            title = 'Reconnaissance de texte')
        self.window = window

        # bouton menu
        menu_button = Gtk.Button.new_from_icon_name(
            'open-menu-symbolic',
            Gtk.IconSize.MENU)

        menu_button.connect('clicked', self.show_menu)
        self.pack_end(menu_button)

    def show_menu (self, obj):

        popover = Gtk.Popover(relative_to = obj)
        popover_box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            border_width = 6)

        about_button = Gtk.ModelButton('À propos')
        about_button.connect('clicked', self.show_about_dialog)

        quit_button = Gtk.ModelButton('Quitter')
        quit_button.connect('clicked', Gtk.main_quit)

        popover_box.add(about_button)
        popover_box.add(quit_button)
        popover.add(popover_box)
        popover_box.show_all()
        popover.popup()

    def show_about_dialog (self, obj):

        dialog = Gtk.AboutDialog(
            authors = ['François Grabenstaetter', 'Danyl El-Kabyr'],
            license_type = Gtk.License.GPL_3_0,
            version = VERSION,
            modal = True,
            transient_for = self.window,
            logo_icon_name = 'system-search-symbolic',
            comments = 'Un utilitaire de reconnaissance de texte pour le projet de POO2')

        dialog.show()
