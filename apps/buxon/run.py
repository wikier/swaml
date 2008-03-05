#!/usr/bin/python
# -*- coding: utf8 -*-

# Buxon, a sioc:Forum Visor
#
# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2006-2008 Sergio Fernández, Diego Berrueta
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

"""Buxon, a sioc:Forum browser"""

import sys
import os
import logging
import pygtk
pygtk.require('2.0')
from gazpacho.loader.loader import ObjectBuilder

try:
    import rdflib
    from rdflib import sparql, Namespace
except:
    print 'RDFLib is required'
    sys.exit(-1)

#global vars
widgets = None
callbacks = None
buxon = None

class Callbacks:

    def destroy(self):
        return buxon.destroy()

    def goButtonClicked(self):
        uri = widgets.get_widget('urlInput').get_text()
        if (uri != ''):
            buxon.clear()
            buxon.clearSearchForm()
            buxon.messageBar( 'query on ' + uri)
            buxon.uri = uri
            buxon.drawTree(buxon.getPosts(uri))

    def searchButtonClicked(self):
        uri = buxon.getUri()
        if (uri != None):
            buxon.clear()
            buxon.text.get_buffer().set_text('')
            text = widgets.get_widget('searchInput').get_text()
            min, max = buxon.getDates()
            buxon.drawTree(buxon.getPosts(uri, min, max, text))

    def selectRow(self, path, column):
        buxon.showPost()

    def fromButtonClicked(self):
        from buxon.ui.calendarwindow import CalendarWindow
        CalendarWindow(widgets.get_widget('fromEntry'))

    def toButtonClicked(self):
        from buxon.ui.calendarwindow import CalendarWindow
        CalendarWindow(widgets.get_widget('toEntry'))

    def alertButtonClicked(self):
        buxon.alertWindow.destroy()


class BuxonMain:

    def __init__(self, argv, base='./'):
        """
        All operation that Buxon need to run
        """

        #configure buxon logger
        self.logger = logging.getLogger('buxon')
        self.logger.setLevel(logging.DEBUG)
        _hdlr = logging.StreamHandler()
        _hdlr.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s'))
        self.logger.addHandler(_hdlr)

        self.logger.info('Starting up Buxon')

        sys.path.append(base + 'src')
        
        from buxon.ui.buxonwindow import BuxonWindow

        try:
            global widgets
            global callbacks
            global buxon

            widgets = ObjectBuilder(base + 'includes/ui/graphical/buxon.glade')
            callbacks = Callbacks()
            widgets.signal_autoconnect(Callbacks.__dict__)
            self.logger.debug('GUI loaded')

            buxon = BuxonWindow(widgets, base)

            if ('-h' in argv or '--help' in argv):
                buxon.usage()

            if (len(argv)>0):
                buxon.main(argv[0])
            else:
                buxon.main()

        except KeyboardInterrupt:
            self.logger.info('Received Ctrl+C or another break signal. Exiting...')
            sys.exit()


if __name__ == '__main__':
    BuxonMain(sys.argv[1:])

