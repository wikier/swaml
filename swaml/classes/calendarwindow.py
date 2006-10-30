#!/usr/bin/python
#
# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2005-2006 Sergio Fdez
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

"""gtk.CalendarWindow"""

import sys
import gtk, pygtk
import time

class CalendarWindow:
    
    def selectDay(self, widget):
        self.window.destroy()
    
    def destroy(self, widget):
        self.setText(self.getDate())
        
    def setText(self, text):
        self.entry.set_text(text)
        
    def getDate(self):
        year, month, day = self.calendar.get_date()
        return str(day) + '/' + str(month+1) + '/' + str(year)
    
    def __init__(self, entry):
        self.entry = entry
        self.window = gtk.Window(gtk.WINDOW_POPUP)
        self.window.connect('destroy', self.destroy)    
        self.window.set_position(gtk.WIN_POS_MOUSE)
        
        self.calendar = gtk.Calendar()
        self.calendar.connect('day_selected_double_click', self.selectDay)
        self.window.add(self.calendar)
        self.calendar.show()
        
        self.window.show()

