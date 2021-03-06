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

"""gtk.CalendarWindow"""

import sys
import gtk, pygtk
import time

class CalendarWindow:
    
    def selectDay(self, widget):
        """
        Select a day
        
        @param widget: widget
        """
        
        self.window.destroy()
    
    def destroy(self, widget):
        """
        Destroy window
        
        @param widget: widget
        """
        
        self.setText(self.getDate())
        
    def setText(self, text):
        """
        Set text on text entry
        
        @param text: text
        """
        
        self.entry.set_text(text)
        
    def getDate(self):
        """
        Get selected date
        
        @return: date in string format
        """
        
        year, month, day = self.calendar.get_date()
        return str(day) + '/' + str(month+1) + '/' + str(year)
    
    def setInitialDate(self):
        """
        Load initial date
        """
        
        date = self.entry.get_text().split('/')
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        
        if (self.calendar != None):
            self.calendar.select_month(month-1, year)
            self.calendar.select_day(day)
    
    def __init__(self, entry):
        """
        CalendarWindow constructor
        """
        
        self.entry = entry
        
        self.window = gtk.Window(gtk.WINDOW_POPUP)
        self.window.connect('destroy', self.destroy)    
        self.window.set_position(gtk.WIN_POS_MOUSE)
        self.window.set_modal(True)
        self.window.set_resizable(False)
        
        self.calendar = gtk.Calendar()
        self.calendar.connect('day_selected_double_click', self.selectDay)
        self.setInitialDate()
        self.window.add(self.calendar)
        self.calendar.show()
        
        self.window.show()

