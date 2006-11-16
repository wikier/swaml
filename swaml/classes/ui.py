#!/usr/bin/env python2.4
# -*- coding: utf8 -*-
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

"""Common functions for UIs"""

import sys, os, string
import pygtk
pygtk.require('2.0')
import gtk

class UI:
    
    def usage(self):
        pass
    
    def __init__(self, id=None, base='./'):
        self.id = id
        self.base = base
    
    
class CommandLineUI(UI):
    
    def usage(self):
        path = self.base + 'usage/' + self.id + '.txt'
        
        try:
            for line in open(path):
                print line,
        except IOError, details:
                print 'Problem reading from ' + path + ': ' + str(details)
                
        sys.exit()
        
    
    def __init__(self, id=None, base='./'):
        UI.__init__(self, id, base+'includes/ui/line/')

    
class GtkUI(UI):
    
    def usage(self):
        path = self.lineBase + 'usage/' + self.id + '.txt'
        
        try:
            for line in open(path):
                print line,
        except IOError, details:
                print 'Problem reading from ' + path + ': ' + str(details)
                
        sys.exit()
    
    def alert(self, text):
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
        self.alertWindow.destroy() 
    
    def __init__(self, id=None, base='./'):
        UI.__init__(self, id, base)
        self.lineBase = self.base + 'includes/ui/line/'
        self.graphicalBase = self.base + 'includes/ui/graphical/'
    