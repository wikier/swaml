#!/usr/bin/env python2.4
#
# GSR <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2006 Sergio Fdez, Diego Berrueta
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
__author__ = 'Diego Berrueta <http://www.berrueta.net/>'

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
		if (url != ''):
			gsr.messageBar( 'query on ' + url)
			gsr.drawTree(url)
			
	def selectRow(self, path, column):
		 gsr.showPost()
	

class Cache:

	def query(self):
		try:
			self.graph = self.loadMailingList(self.uri)
			self.loadAdditionalData(self.uri)
			
			print 'Total triples loaded:', len(self.graph)
	
			sparqlGr = sparql.sparqlGraph.SPARQLGraph(self.graph)
			select = ('?post', '?postTitle', '?userName', '?parent')			
			where  = sparql.GraphPattern([('?post',	RDF['type'],		SIOC['Post']),
										  ('?post',	SIOC['title'],		'?postTitle'),
										  ('?post',	SIOC['has_creator'],'?user'),
										  ('?user', SIOC['name'], 		'?userName')])
			opt    = sparql.GraphPattern([('?post',	SIOC['reply_of'],	'?parent')])
			posts  = sparqlGr.query(select, where, opt)
			return posts			
		except Exception, details:
			gsr.messageBar('unknow problem parsing RDF at ' + self.uri)
			print 'parsing exception:', str(details)
			return None
		
	def getPost(self, uri):
		#FIXME
		return uri
	
	def loadMailingList(self, uri):
	    graph = rdflib.Graph()
	    print 'Getting mailing list data (', uri, ')...',
	    graph.parse(uri)
	    print 'OK, loaded', len(graph), 'triples'
	    return graph
	
	def loadAdditionalData(self, uri):
	
	    for post in self.graph.objects(uri, SIOC['container_of']):
	        if not self.hasValueForPredicate(post, SIOC['title']):
	            print 'Resolving reference to get additional data (', post, ')...',
	            self.graph.parse(post)
	            print 'OK, now', len(self.graph), 'triples'
	
	    for user in self.graph.objects(uri, SIOC['has_subscriber']):
	        if not self.hasValueForPredicate(user, SIOC['email_sha1sum']):
	            print 'Resolving reference to get additional data (', user, ')...',
	            self.graph.parse(user)
	            print 'OK, now', len(self.graph), 'triples'	

	def hasValueForPredicate(self, subject, predicate):
	    return (len([x for x in self.graph.objects(subject, predicate)]) > 0)	          

	def __init__(self, uri):
		self.uri = uri
		

class GSR:

	def showPost(self):
		selection = self.treeView.get_selection()
		(model, iter) = selection.get_selected()
		uri = model.get_value(iter, 0)
		self.write(self.cache.getPost(uri))

	def drawTree(self, url):
		self.cache = Cache(url)
		posts = self.cache.query()
		
		if (posts!=None and len(posts)>0):
		
			#create view and model
			self.treeView = widgets.get_widget('postsTree')
			self.treeStore = gtk.TreeStore(str, str)
			self.treeView.set_model(self.treeStore)
			
			#append items
			parent = None
			for (post, title, creator, parent) in posts:
				#bug: it ins't order by date, then the tree is bad builded
				self.treeTranslator[post] = self.treeStore.append(self.__getParent(parent), [str(post), str(title)])
				
			#and show it
			treeColumn = gtk.TreeViewColumn('Posts')
			self.treeView.append_column(treeColumn)
			cell = gtk.CellRendererText()
			treeColumn.pack_start(cell, True)
			treeColumn.add_attribute(cell, 'text', 1)
			treeColumn.set_sort_column_id(0)
			
			self.messageBar('loaded ' + url)
			
		else:
			
			self.messageBar('none posts founded at ' + url)
			
	def __getParent(self, uri):
		if (uri in self.treeTranslator):
			return self.treeTranslator[uri]
		else:
			return None
	
	def messageBar(self, text):
		self.statusbar.push(0, text)
		
	def write(self, text):
		buffer = self.text.get_buffer()
		buffer.set_text(text + ' (FIXME)')

	def main(self, uri=None):
		if (uri != None):
			self.input.set_text(uri)
		gtk.main()

	def __init__(self):
		
		self.treeTranslator = {}
		
		#widgets
		self.text = widgets.get_widget('swamlViewer')
		self.input = widgets.get_widget('urlInput')
		self.statusbar = widgets.get_widget('gsrStatusbar')
		self.messageBar('ready')
	
		#main window
		self.window = widgets.get_widget('gsr')
		self.window.set_icon_from_file('rdf.ico')
		self.window.show()
		

#RDFlib namespaces
RDF = Namespace(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
SIOC = Namespace(u'http://rdfs.org/sioc/ns#')
		
#and all necessary for PyGTK
widgets = ObjectBuilder('gsr.glade')
callbacks = Callbacks()
widgets.signal_autoconnect(Callbacks.__dict__)
gsr = GSR()	

if __name__ == '__main__':
	try:
		if (len(sys.argv)>1):
			gsr.main(sys.argv[1])
		else:
			gsr.main()
	except KeyboardInterrupt:
		print 'Received Ctrl+C or another break signal. Exiting...'
		sys.exit()
