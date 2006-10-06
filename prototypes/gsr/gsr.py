#!/usr/bin/env python2.4
#
# GSR <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2006 Sergio Fdez
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

__author__ = 'Sergio Fdez <http://www.wikier.org/>'

import sys
import pygtk
pygtk.require('2.0')
import gtk
from gazpacho.loader.loader import ObjectBuilder

widgets = ObjectBuilder('gsr.glade')

class Callbacks:

	def destroy(self):
		print 'Exiting...'
		gtk.main_quit()

	def goButtonClicked(self):
		print widgets.get_widget('urlInput').get_text()

	def __init__(selfs):
		pass

callbacks = Callbacks()
widgets.signal_autoconnect(Callbacks.__dict__)

class GSR:

	def drawTree(self):
		#http://www.pygtk.org/pygtk2tutorial-es/examples/basictreeview.py
		pass

	def main(self):
		self.drawTree()
		gtk.main()

	def __init__(self, widgets):
		self.widgets = widgets
	
		#main window
		self.window = self.widgets.get_widget('gsr')
		self.window.set_title('GSR')
		self.window.show()


if __name__ == '__main__':

	gsr = GSR(widgets)	
	try:
		gsr.main()
	except KeyboardInterrupt:
		print 'Received Ctrl+C or another break signal. Exiting...'
		sys.exit()
