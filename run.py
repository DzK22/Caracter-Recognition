#!/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from ui.window import Window

GLib.set_prgname('Reconnaissance de texte')

win = Window()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()
