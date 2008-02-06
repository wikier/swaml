# -*- coding: utf8 -*-
#
# Buxon, a sioc:Forum Visor
#
# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2005-2008 Sergio Fernández
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

from buxon.ui.ui import UI
		
class GtkUI(UI):
    """
    Abstract class for GTK User Interfaces
    """    
    
    def usage(self):
        """
        Print usage information
        """
                
        path = self.lineBase + 'usage/' + self.id + '.txt'
        
        try:
            for line in open(path):
                print line,
        except IOError, details:
                print 'Problem reading from ' + path + ': ' + str(details)
                
        sys.exit()
    
    def alert(self, text):
        """
        Alert window
        
        @param text: text on alert
        """
        
        self.alertWindow = gtk.Window(gtk.WINDOW_POPUP)
        self.alertWindow.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.alertWindow.set_modal(True)
        self.alertWindow.set_resizable(False)
        self.alertWindow.set_border_width(0)
        
        vbox = gtk.VBox(False, 5)
        vbox.set_border_width(10)
        self.alertWindow.add(vbox)
        vbox.show()
                
        align1 = gtk.Alignment(0.5, 0.5, 0, 0)
        vbox.pack_start(align1, False, False, 5)
        align1.show()
        label = gtk.Label(text)
        align1.add(label)
        label.show()
        
        align2 = gtk.Alignment(0.5, 0.5, 0, 0)
        vbox.pack_start(align2, False, False, 5)
        align2.show()        
        button = gtk.Button('OK')
        button.connect('clicked', self.destroyAlert, 'cool button')
        align2.add(button)
        button.show()
        
        self.alertWindow.show()
        
    def destroyAlert(self, widget=None, other=None):
        """
        Destroy aler window
        
        @param widget: widget
        @param other: other
        """
        
        self.alertWindow.destroy() 
    
    def __init__(self, id=None, base='./'):
        """
        Constructor method
        
        @param id: string id
        @param base: base directory
        """
                
        UI.__init__(self, id, base)
        self.lineBase = self.base + 'includes/ui/text/'
        self.graphicalBase = self.base + 'includes/ui/graphical/'

