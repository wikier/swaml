# -*- coding: utf8 -*-
#
# Buxon, a sioc:Forum Visor
#
# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2006-2007 Sergio Fernández, Diego Berrueta
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
from buxon.rdf.fetcher import Fetcher
from buxon.rdf.namespaces import SIOC, RDF, RDFS, DC, DCTERMS
from buxon.common.date import MailDate

class Cache:

	def orderByDate(self, posts):
		"""
 		Order by date a list of posts
		
		@param posts: posts to order
		@return: posts ordered
		"""
		
		#SPARQL in RDFLib doesn't support 'ORDER BY' queries
		#then we'll implement a rustic support to order by dates
		#state: testing
        
		#extract dates in integer long format
		dict = {}
		dates = []
		for (post, title, date, creator, content, parent) in posts:
			intDate = MailDate(date).getInteger()
			dates.append(intDate)
			dict[intDate] = (post, title, date, creator, content, parent)
            
		#and we put ordered into a new list
		dates.sort()
		ordered = [] 
		for date in dates:
			ordered.append(dict[date])
            
		return ordered
            
	def filterPosts(self, posts, min=None, max=None, text=None):
		"""
		Filter post from some conditions
        
		@param posts: list of posts
 		@param min: min date
		@param max: max date
		@param text: text to search
		"""
        
		filtered = []
        
		for (post, title, date, creator, content, parent) in posts:
            
			intDate = MailDate(date).getInteger()
            
			#exist if date is bigger
			if (max!=None and intDate>max):
				break
            
			#continue if is smaller
			if  (min!=None and intDate<min):
				continue
            
			#and then filter by text
			if (text == None):
				filtered.append((post, title, date, creator, content, parent))
 			else:
 				if (self.__like(title,text) or self.__like(content,text)):
					filtered.append((post, title, date, creator, content, parent))
            
 		return filtered

	def __like(self, text, query):
		"""
        Search words into a text
        
        @param text: text where we'll search
        @param query: words to search
		"""
        
 		text = text.lower()
		query = query.lower().split(' ')
        
		for one in query:
 			if not one in text:
 				return False
        
		return True

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

	def query(self):
		"""
		Make a SPARQL query
        
		@return: posts result
		"""
        
 		try:
			sparqlGr = SPARQLGraph(self.graph)
			select = ('?post', '?postTitle', '?date', '?userName', '?content', '?parent')            
			where  = GraphPattern([('?post',    RDF['type'],            SIOC['Post']),
                                          ('?post',    DC['title'],            '?postTitle'),
                                          ('?post',    DCTERMS['created'],     '?date'),
                                          ('?post',    SIOC['content'],        '?content'),
                                          ('?post',    SIOC['has_creator'],    '?user'),
                                          ('?user',    SIOC['name'],           '?userName')])
			opt    = GraphPattern([('?post',    SIOC['reply_of'],       '?parent')])
			posts = Query.query(sparqlGr, select, where, opt)
			return self.orderByDate(posts)
		except Exception, details:
			print 'parsing exception:', str(details)
			return None
        
	def getPostAuthor(self, post):
		"""
        Get author of a post
        
        @param post: post uri
		"""
        
		authorUri = self.getValueForPredicate(post, SIOC['has_creator'])
		author = self.getValueForPredicate(authorUri, SIOC['name'])
		return author, authorUri
        
	def getPost(self, uri):
		"""
        Get fields of a post
        
        @param uri: post uri
        @return: post fields
 		"""
        
		author, authorUri = self.getPostAuthor(uri)
		listUri = self.getValueForPredicate(uri, SIOC['has_container'])
 		listName = self.getValueForPredicate(listUri, DC['title'])
		title = self.getValueForPredicate(uri, DC['title'])
		date = self.getValueForPredicate(uri, DCTERMS['created'])
		content = self.getValueForPredicate(uri, SIOC['content'])
		return author, authorUri, listName, listUri, title, date, content

	def dump(self, path='cache.rdf'):
 		"""
        Dump graph on disk
        
        @param path: path to dump
 		"""
        
		if bool(self.graph):
			try:
				file = open(path, 'w+')
 				self.graph.serialize(destination=file, format="pretty-xml")
				file.flush()
				file.close()
 			except IOError, detail:
				print 'Error dumping cache: ' + str(detail)

	def __init__(self, uri, ping, pb=None):
		"""
		Cache constructor
		
		@param uri: uri to load
		@param pb: progress bar
		"""
		
		self.uri = uri
		fetcher = Fetcher(uri, ping, pb)
		self.graph = fetcher.getData()

