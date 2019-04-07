import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from ui.headerBar import HeaderBar
from ui.content import Content

class Window (Gtk.Window):

    def __init__ (self):
        Gtk.Window.__init__(self,
            resizable = False,
            default_width = 700,
            default_height = 400)

        self.content = Content(self)
        self.header_bar = HeaderBar(self)
        self.set_titlebar(self.header_bar)
        self.add(self.content)

        # Chargement du CSS
        with open('ui/style.css') as file:
            css = file.read()
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_data(css.encode())
        Gtk.StyleContext().add_provider_for_screen(
            Gdk.Screen.get_default(),
            cssProvider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER)
