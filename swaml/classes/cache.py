#!/usr/bin/env python2.4
# -*- coding: utf8 -*-
#
# SWAML <http://swaml.berlios.de/>
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

"""a cache service for sioc:Forum"""

import rdflib
from rdflib import sparql, Namespace
from namespaces import SIOC, RDF, RDFS, DC, DCTERMS
from dateutils import MailDate
import gtk

class Cache:

    def orderByDate(self, posts):
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
        text = text.lower()
        query = query.lower().split(' ')
        
        for one in query:
            if not one in text:
                return False
        
        return True

    def query(self):
        try:    
            sparqlGr = sparql.sparqlGraph.SPARQLGraph(self.graph)
            select = ('?post', '?postTitle', '?date', '?userName', '?content', '?parent')            
            where  = sparql.GraphPattern([('?post',    RDF['type'],            SIOC['Post']),
                                          ('?post',    DC['title'],          '?postTitle'),
                                          ('?post',    DCTERMS['created'],     '?date'),
                                          ('?post',    SIOC['content'],        '?content'),
                                          ('?post',    SIOC['has_creator'],    '?user'),
                                          ('?user',    SIOC['name'],           '?userName')])
            opt    = sparql.GraphPattern([('?post',    SIOC['reply_of'],       '?parent')])
            posts  = sparqlGr.query(select, where, opt)
            return self.orderByDate(posts)
        except Exception, details:
            print 'parsing exception:', str(details)
            return None
        
    def __listPosts(self):
        try:    
            sparqlGr = sparql.sparqlGraph.SPARQLGraph(self.graph)
            select = ('?post', '?title')            
            where  = sparql.GraphPattern([('?post', RDF['type'],   SIOC['Post']),
                                          ('?post', DC['title'], '?title')])
            posts  = sparqlGr.query(select, where)
            
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
        
    def getPostAuthor(self, post):
        authorUri = self.getValueForPredicate(post, SIOC['has_creator'])
        author = self.getValueForPredicate(authorUri, SIOC['name'])
        return author, authorUri
        
    def getPost(self, uri):
        author, authorUri = self.getPostAuthor(uri)
        listUri = self.getValueForPredicate(uri, SIOC['has_container'])
        listName = self.getValueForPredicate(listUri, DC['title'])
        title = self.getValueForPredicate(uri, DC['title'])
        date = self.getValueForPredicate(uri, DCTERMS['created'])
        content = self.getValueForPredicate(uri, SIOC['content'])
        return author, authorUri, listName, listUri, title, date, content
    
    def loadMailingList(self, uri):
        graph = rdflib.Graph()
        print 'Getting mailing list data (', uri, ')...',
        graph.parse(uri)
        print 'OK, loaded', len(graph), 'triples'
        if (self.pb != None):
            self.pb.progress()
        return graph
    
    def __loadData(self, uri):
        print 'Resolving reference to get additional data (', uri, ')...',
        self.graph.parse(uri)
        
        if (self.pb != None):
            self.pb.progress()
            while gtk.events_pending():
                gtk.main_iteration()
                
        print 'OK, now', len(self.graph), 'triples'     
    
    def loadAdditionalData(self):
    
        for post in self.graph.objects(self.uri, SIOC['container_of']):
            if not self.hasValueForPredicate(post, SIOC['id']):
                postSeeAlso = self.getValueForPredicate(post, RDFS['seeAlso'])
                if (postSeeAlso == None):
                    self.__loadData(post)
                else:
                    self.__loadData(postSeeAlso)
    
        for user in self.graph.objects(self.uri, SIOC['has_subscriber']):
            if not self.hasValueForPredicate(user, SIOC['email_sha1sum']):
                self.__loadData(user)

    def hasValueForPredicate(self, subject, predicate):
        return (len([x for x in self.graph.objects(subject, predicate)]) > 0)        
       
    def getValueForPredicate(self, subject, predicate):
        value = [x for x in self.graph.objects(subject, predicate)]
        if (len(value) > 0):
            return value[0]
        else:
            return None
        
    def dump(self, path='cache.rdf'):
        if (not self.bad):
            try:
                file = open(path, 'w+')
                self.graph.serialize(destination=file, format="pretty-xml")
                file.flush()
                file.close()
            except IOError, detail:
                print 'Error dumping cache: ' + str(detail)

    def __init__(self, uri, pb=None):
        self.uri = uri
        self.bad = False
        self.pb = pb
        
        
        try:
            self.graph = self.loadMailingList(self.uri)
        except Exception, details:
            print '\nAn exception ocurred parsing ' + uri + ': ' + str(details)
            self.bad = True
            return
        
        self.loadAdditionalData()
        
        self.__listPosts()
        
        if (self.pb != None):
            self.pb.destroy()
        
        print 'Total triples loaded:', len(self.graph)
