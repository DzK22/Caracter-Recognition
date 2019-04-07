#!/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from ui.window import Window
from ui.env import *

GLib.set_prgname(PROGRAM_NAME)
win = Window()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()
