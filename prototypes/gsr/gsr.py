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
from dates import MailDate


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

	def orderByDate(self, graph, min=None, max=None):
		#SPARQL in RDFLib doesn't support 'ORDER BY' queries
		#then we'll implement a rustic support to order by dates
		#state: testing
		
		#extract dates in integer long format
		dict = {}
		dates = []
		for (post, title, date, creator, parent) in graph:
			intDate = MailDate(date).getInteger()
			dates.append(intDate)
			dict[intDate] = (post, title, date, creator, parent)
			
		#and we put ordered into a new list
		dates.sort()
		ordered = [] 
		for date in dates:
			if (min!=None and max!=None):
				if (date>=min and date<=max):
					ordered.append(dict[date])
			else:
				ordered.append(dict[date])
			
		return ordered

	def query(self, min=None, max=None):
		try:	
			sparqlGr = sparql.sparqlGraph.SPARQLGraph(self.graph)
			select = ('?post', '?postTitle', '?date', '?userName', '?parent')			
			where  = sparql.GraphPattern([('?post',	RDF['type'],		SIOC['Post']),
										  ('?post',	SIOC['title'],		'?postTitle'),
										  ('?post', DCTERMS['created'],	'?date'),
										  ('?post',	SIOC['has_creator'],'?user'),
										  ('?user', SIOC['name'], 		'?userName')])
			opt    = sparql.GraphPattern([('?post',	SIOC['reply_of'],	'?parent')])
			posts  = sparqlGr.query(select, where, opt)
			return self.orderByDate(posts, min, max)
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
		self.graph = self.loadMailingList(self.uri)
		self.loadAdditionalData(self.uri)
		print 'Total triples loaded:', len(self.graph)		
		

class GSR:

	def showPost(self):
		selection = self.treeView.get_selection()
		(model, iter) = selection.get_selected()
		uri = model.get_value(iter, 0)
		self.write(self.cache.getPost(uri))
		
	def getSpinValues(self):
		
		#min date
		fromDay = widgets.get_widget('fromDaySpin')
		fromMonth = widgets.get_widget('fromMonthSpin')
		fromYear = widgets.get_widget('fromYearSpin')
		min  = fromYear.get_value_as_int() * 10000000000
		min += fromMonth.get_value_as_int()* 100000000
		min += fromDay.get_value_as_int()  * 1000000

		#max date
		toDay = widgets.get_widget('toDaySpin')
		toMonth = widgets.get_widget('toMonthSpin')
		toYear = widgets.get_widget('toYearSpin')
		max  = toYear.get_value_as_int() * 10000000000
		max += toMonth.get_value_as_int()* 100000000
		max += toDay.get_value_as_int()  * 1000000
		
		return min, max	

	def drawTree(self, uri):
		if (self.cache == None):
			self.cache = Cache(uri)
		else:
			if (uri != self.cache.uri):
				self.cache = Cache(uri)
		min, max = self.getSpinValues()
		posts = self.cache.query(min, max)
		
		if (posts!=None and len(posts)>0):
		
			#create view and model
			self.treeView = widgets.get_widget('postsTree')
			for column in self.treeView.get_columns():
				self.treeView.remove_column(column)
			self.treeStore = gtk.TreeStore(str, str)
			self.treeView.set_model(self.treeStore)
			
			#append items
			parent = None
			for (post, title, date, creator, parent) in posts:
				self.treeTranslator[post] = self.treeStore.append(self.__getParent(parent), [str(post), str(title)])
				print 'drawing post', post, 'on tree'

			#and show it
			treeColumn = gtk.TreeViewColumn('Posts')
			self.treeView.append_column(treeColumn)
			cell = gtk.CellRendererText()
			treeColumn.pack_start(cell, True)
			treeColumn.add_attribute(cell, 'text', 1)
			treeColumn.set_sort_column_id(0)
			
			self.messageBar('loaded ' + uri)
			
		else:
			
			self.messageBar('none posts founded at ' + uri)
			
	def __getParent(self, uri):
		if (uri in self.treeTranslator):
			return self.treeTranslator[uri]
		else:
			return None
	
	def messageBar(self, text):
		self.statusbar.push(0, text)

	def write(self, text):
		data = '<html><head><title>GSR</title></head><body>' + text + '</body></html>'
		self.moz.render_data(data, long(len(data)), 'file:///', 'text/html')
		
	def createGecko(self):
		import gtkmozembed # http://sourceforge.net/projects/pygtkmoz
		self.contentBox = widgets.get_widget('contentBox')
		self.moz = gtkmozembed.MozEmbed()
		self.contentBox.pack_end(self.moz, False, False, 0)
		self.moz.show()

	def main(self, uri=None):
		if (uri != None):
			self.input.set_text(uri)
		gtk.main()

	def __init__(self):
		
		self.cache = None
		self.treeTranslator = {}
		
		#widgets
		self.text = widgets.get_widget('swamlViewer')
		self.input = widgets.get_widget('urlInput')
		self.createGecko()
		self.statusbar = widgets.get_widget('gsrStatusbar')
		self.messageBar('ready')
	
		#main window
		self.window = widgets.get_widget('gsr')
		self.window.set_icon_from_file('rdf.ico')
		self.window.show()
		

#RDFlib namespaces
RDF = Namespace(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
SIOC = Namespace(u'http://rdfs.org/sioc/ns#')
DCTERMS = Namespace(u'http://purl.org/dc/terms/')
		
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
