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
import rdflib
from rdflib import sparql, Namespace


class Callbacks:

	def destroy(self):
		print 'Exiting...'
		gtk.main_quit()
		return gtk.FALSE

	def goButtonClicked(self):
		url = widgets.get_widget('urlInput').get_text()
		if (url != ""):
			gsr.messageBar( 'query on ' + url)
			gsr.drawTree(url)
			
	def selectRow(self):
		 gsr.showMessage()
	

class Cache:

	def query(self):
		self.graph = rdflib.Graph()
		try:
			self.graph.parse(self.url)
		except:
			gsr.messageBar('unknow problem parsing RDF at ' + self.url)

		RDF = Namespace(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
		SIOC = rdflib.Namespace(u'http://rdfs.org/sioc/ns#')

		sparqlGr = sparql.sparqlGraph.SPARQLGraph(self.graph)
		select = ("?postUri")
		where  = sparql.GraphPattern([("?x", RDF["type"], SIOC["Forum"]), ("?x", SIOC["container_of"], "?postUri")])
		self.posts  = sparqlGr.query(select, where)
		return self.posts

	def __init__(self, url):
		self.url = url
		

class GSR:

	def showMessage(self):
		selection = self.treeView.get_selection()
		(model, iter) = selection.get_selected()
		print model, iter

	def drawTree(self, url):
		self.cache = Cache(url)
		posts = self.cache.query()
		
		#create view and model
		self.treeView = widgets.get_widget('postsTree')
		self.treeStore = gtk.TreeStore(str)
		self.treeView.set_model(self.treeStore)
		
		#append items
		parent = None
		for uri in posts:
			new = self.treeStore.append(None, [str(uri)])
			
		#and show it
		treeColumn = gtk.TreeViewColumn('Posts')
		self.treeView.append_column(treeColumn)
		cell = gtk.CellRendererText()
		treeColumn.pack_start(cell, True)
		treeColumn.add_attribute(cell, 'text', 0)
		treeColumn.set_sort_column_id(0)
		
		self.messageBar('loaded ' + url)
		
	
	def messageBar(self, text):
		self.statusbar.push(0, text)

	def main(self):
		gtk.main()

	def __init__(self):
		
		#statusbar
		self.statusbar = widgets.get_widget('gsrStatusbar')
		self.messageBar('ready')
	
		#main window
		self.window = widgets.get_widget('gsr')
		self.window.set_icon_from_file('rdf.ico')
		self.window.show()
		
		
		
widgets = ObjectBuilder('gsr.glade')
callbacks = Callbacks()
widgets.signal_autoconnect(Callbacks.__dict__)
gsr = GSR()	

if __name__ == '__main__':
	try:
		gsr.main()
	except KeyboardInterrupt:
		print 'Received Ctrl+C or another break signal. Exiting...'
		sys.exit()
