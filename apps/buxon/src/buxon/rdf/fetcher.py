# -*- coding: utf8 -*-
#
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

"""a cache service for sioc:Forum"""

from rdflib import URIRef
from rdflib.Graph import ConjunctiveGraph
from rdflib.sparql.sparqlGraph import SPARQLGraph
from rdflib.sparql.graphPattern import GraphPattern
from rdflib.sparql import Query
from rdflib import Namespace
from buxon.rdf.namespaces import SIOC, RDF, RDFS, DC, DCTERMS
from buxon.rdf.ptsw import PTSW
import socket
import gtk

class Fetcher:
        
	def __listPosts(self):
		"""
        List post at cache
		"""
        
		try:    
			sparqlGr = SPARQLGraph(self.graph)
			select = ('?post', '?title')            
			where  = GraphPattern([('?post', RDF['type'],   SIOC['Post']),
                                          ('?post', DC['title'], '?title')])
			posts = Query.query(sparqlGr, select, where)
            
 			print len(posts), 'posts:'
            
			for post, title in posts:
				print post, 
				try:
					print title
				except:
					print '(bad formed title)'
                
		except Exception, details:
 			print 'parsing exception:', str(details)
			return None
	
    
	def loadMailingList(self, uri):
		"""
        Load a mailing list into a graph memory
        
        @param uri: mailing list's uri
		"""
        
		graph = ConjunctiveGraph()
		print 'Getting mailing list data (', uri, ')...',
		graph.parse(uri)
		print 'OK, loaded', len(graph), 'triples'
        
		self.uri = self.__getForums(graph)[0]
		print 'Using ' + self.uri + ' sioc:Forum'
        
 		if (self.pb != None):
 			self.pb.progress()
            
		if (self.ptsw != None):
			self.ptsw.ping(uri)
        
		return graph
    
	def __loadData(self, uri):
		"""
		Load data
        
		@param uri: uri to load
		"""
        
 		print 'Resolving reference to get additional data (', uri, ')...',
		try:
			self.graph.parse(uri)
		except:
			print '\nAn exception ocurred parsing ' + uri
			return
        
		if (self.pb != None):
 			self.pb.progress()
			while gtk.events_pending():
				gtk.main_iteration()
        
		if (self.ptsw != None):
			self.ptsw.ping(uri)
                
		print 'OK, now', len(self.graph), 'triples'    
        
	def __getForums(self, graph): 
		"""
        Get all sioc:Forum's in a graph
		"""
        
		sparqlGr = SPARQLGraph(graph)
		select = ('?uri')
		where  = GraphPattern([('?uri', RDF['type'], SIOC['Forum'])])
		forums = Query.query(sparqlGr, select, where)
		return forums;
        
    
	def loadAdditionalData(self):
		"""
        Load additional data of a mailing list
		"""
        
		for post in self.graph.objects(self.uri, SIOC['container_of']):
			if not self.hasValueForPredicate(post, SIOC['id']):
				postSeeAlso = self.getValueForPredicate(post, RDFS['seeAlso'])
				if (postSeeAlso == None):
					self.__loadData(post)
				else:
					self.__loadData(postSeeAlso)
        
 		for user in self.graph.objects(predicate=SIOC['has_subscriber']):
			if not self.hasValueForPredicate(user, SIOC['email_sha1']):
 				self.__loadData(user)

	def hasValueForPredicate(self, subject, predicate):
		"""
		Get if a predicate exists
        
 		@param subject: subject
 		@param predicate: predicate
		"""
        
		return (len([x for x in self.graph.objects(URIRef(subject), predicate)]) > 0)        
       
	def getValueForPredicate(self, subject, predicate):
		"""
        Get value of a predicate
        
        @param subject: subject
        @param predicate: predicate
		"""        
        
		value = [x for x in self.graph.objects(URIRef(subject), predicate)]
		if (len(value) > 0):
			return value[0]
		else:
			return None

	def getData(self):
        
		try:
			self.graph = self.loadMailingList(self.uri)
		except Exception, details:
 			print '\nAn exception ocurred parsing ' + self.uri + ': ' + str(details)
			self.bad = True
 			return
        
		self.loadAdditionalData()
        
		#self.__listPosts()
        
		if (self.pb != None):
			self.pb.destroy()
        
		if (self.ptsw != None):
			print self.ptsw.stats()

		if self.bad:
			return None
		else:
			print 'Total triples loaded:', len(self.graph)
			return self.graph

	def __init__(self, base, ping, pb=None):
		"""
		Cache constructor
		
		@param base: base uri to load
		@param pb: progress bar
        """
		
		self.uri = base
		self.graph = None
		self.bad = False
		self.pb = pb
		self.ptsw = None
		if ping:
			self.ptsw = PTSW()

		socket.setdefaulttimeout(5)

