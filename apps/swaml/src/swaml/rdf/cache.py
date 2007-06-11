# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2006-2007 Sergio Fdez, Diego Berrueta
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
from rdflib import Namespace
from rdflib.sparql import sparqlGraph
from rdflib.sparql.graphPattern import GraphPattern
from rdflib.Graph import ConjunctiveGraph
from swaml.rdf.namespaces import SIOC, RDF, RDFS, DC, DCTERMS
from swaml.common.date import MailDate
from swaml.rdf.ptsw import PTSW
import socket
import gtk

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

    def query(self):
        """
        Make a SPARQL query
        
        @return: posts result
        """
        
        try:    
            sparqlGr = sparqlGraph.SPARQLGraph(self.graph)
            select = ('?post', '?postTitle', '?date', '?userName', '?content', '?parent')            
            where  = GraphPattern([('?post',    RDF['type'],            SIOC['Post']),
                                          ('?post',    DC['title'],            '?postTitle'),
                                          ('?post',    DCTERMS['created'],     '?date'),
                                          ('?post',    SIOC['content'],        '?content'),
                                          ('?post',    SIOC['has_creator'],    '?user'),
                                          ('?user',    SIOC['name'],           '?userName')])
            opt    = GraphPattern([('?post',    SIOC['reply_of'],       '?parent')])
            posts  = sparqlGr.query(select, where, opt)
            return self.orderByDate(posts)
        except Exception, details:
            print 'parsing exception:', str(details)
            return None
        
    def __listPosts(self):
        """
        List post at cache
        """
        
        try:    
            sparqlGr = sparqlGraph.SPARQLGraph(self.graph)
            select = ('?post', '?title')            
            where  = GraphPattern([('?post', RDF['type'],   SIOC['Post']),
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
    
    def loadMailingList(self, uri):
        """
        Load a mailing list into a graph memory
        
        @param uri: mailing list's uri
        """
        
        graph = ConjunctiveGraph()
        print 'Getting mailing list data (', uri, ')...',
        try:
            graph.parse(uri)
            print 'OK, loaded', len(graph), 'triples'
        except:
            print '\nAn exception ocurred parsing ' + uri
            return graph         
        
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
    
        for user in self.graph.objects(self.uri, SIOC['has_subscriber']):
            if not self.hasValueForPredicate(user, SIOC['email_sha1sum']):
                self.__loadData(user)

    def hasValueForPredicate(self, subject, predicate):
        """
        Get if a predicate exists
        
        @param subject: subject
        @param predicate: predicate
        """
        
        return (len([x for x in self.graph.objects(subject, predicate)]) > 0)        
       
    def getValueForPredicate(self, subject, predicate):
        """
        Get value of a predicate
        
        @param subject: subject
        @param predicate: predicate
        """        
        
        value = [x for x in self.graph.objects(subject, predicate)]
        if (len(value) > 0):
            return value[0]
        else:
            return None
        
    def dump(self, path='cache.rdf'):
        """
        Dump graph on disk
        
        @param path: path to dump
        """
        
        if (not self.bad):
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
        self.bad = False
        self.pb = pb
        self.ptsw = None
        if ping:
            self.ptsw = PTSW()
        
        socket.setdefaulttimeout(5)
        
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
        
        if (self.ptsw != None):
            print self.ptsw.stats()
        
        print 'Total triples loaded:', len(self.graph)
