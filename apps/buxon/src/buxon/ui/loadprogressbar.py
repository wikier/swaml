# -*- coding: utf8 -*-

# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2005-2006 Sergio Fernández
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""gtk.ProgressBar for heavy works"""

import sys
import gtk, pygtk, gobject

class LoadProgressBar:
    """
    ProgressBar for load events
    """

    def destroy(self, widget=None):
        """
        Destroy
        
        @param widget: widget
        """
        
        self.window.destroy()
        
    def progress(self):
        """
        Update the value of the progress bar
        """
        
        new_val = self.pbar.get_fraction() + 0.01
        if new_val > 1.0:
            new_val = 0.0
        self.pbar.set_fraction(new_val)
        return True

    def __init__(self):
        """
        PorgressBarLoad constructor
        """
        
        self.window = gtk.Window(gtk.WINDOW_POPUP)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_modal(True)
        self.window.set_resizable(False)

        self.window.connect('destroy', self.destroy)
        self.window.set_border_width(0)

        vbox = gtk.VBox(False, 5)
        vbox.set_border_width(10)
        self.window.add(vbox)
        vbox.show()
  
        # Create a centering alignment object
        align = gtk.Alignment(0.5, 0.5, 0, 0)
        vbox.pack_start(align, False, False, 5)
        align.show()

        # Create the ProgressBar
        self.pbar = gtk.ProgressBar()
        self.pbar.set_text('loading...')
        align.add(self.pbar)
        self.pbar.show()
        
        self.progress()

        self.window.show()
