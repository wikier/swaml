# -*- coding: utf8 -*-

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

"""Util services to work with FOAF"""

import sys, os, string, sha
from rdflib.Graph import ConjunctiveGraph
from rdflib.sparql.sparqlGraph import SPARQLGraph
from rdflib.sparql.graphPattern import GraphPattern
from rdflib.sparql import Query
from rdflib import Namespace, Literal
from swaml.rdf.namespaces import SIOC, RDF, RDFS, FOAF, GEO
from email.rdf.sindice import Sindice
from email.Header import decode_header

class FOAFS:
    """
    Collection of util services to SWAML
    """
    
    def __init__(self):
        """
        FOAF services constructor
        """
        
        self.__actualFoaf = None
        self.__graph = None
    
    def getFoaf(self, mail):
        """
        Services to obtain FOAF URI from an email address
        
        @param mail: an email address
        @type mail: string
        @return: the FOAF URI of this email owner
        @rtype: string
        """
        
        mail_sha1sum = self.getShaMail(mail)
        return self.getFoafFromSha(mail_sha1sum)
        
    def getFoafFromSha(self, mail_sha1sum):
        """
        Obtain FOAF URI from an email sha1sum, provided by sindice.com
        
        @param mail_sha1sum: an email address sha1sum
        @type mail_sha1sum: string
        @return: the FOAF URI of this email owner
        @rtype: string
        """
        
        s = Sindice()
        results = s.lookupIFPs("http://xmlns.com/foaf/0.1/mbox_sha1sum", mail_sha1sum)
                    
        if len(results)>0:
            return results[0][0] #FIXME
        else:
            return None        
        
    def __getGraph(self, foaf):
        """
        A simple mechanism to cache foaf graph
        
        @param foaf: a foaf uri
        @return: the graph with the foaf loaded
        @rtype: rdflib.Graph.ConjunctiveGraph
        """
        
        #tip to set socket timeout global var
        import socket
        socket.setdefaulttimeout(10) #timeout in seconds
        
        if (self.__actualFoaf != foaf or self.__graph == None):
            self.__actualFoaf = foaf
            self.__graph = ConjunctiveGraph()
            try:
                self.__graph.parse(foaf)
            except:
                self.__graph = None
        
        return self.__graph
        
    def getGeoPosition(self, foaf, sha1mail):
        """
        Obtain geography information from foaf
        
        @param foaf: a foaf uri
        @param sha1mail: mail addess enconded
        @return: coordinates      
        """
        
        graph = self.__getGraph(foaf)
        
        if (graph != None):
        
            sparqlGr = SPARQLGraph(graph)
            select = ('?lat', '?long')
            where  = GraphPattern([ ('?x', RDF['type'], FOAF['Person']),
                                    ('?x', FOAF['mbox_sha1sum'], sha1mail),
                                    ('?x', FOAF['based_near'], '?y'),
                                    ('?y', GEO['lat'], '?lat'),
                                    ('?y', GEO['long'], '?long')    
                                  ])
            
            result = Query.query(sparqlGr, select, where)
        
            for one in result:
                return [one[0], one[1]]
        
        return [None, None]
    
    def getPic(self, foaf, sha1mail):
        """
        Get picture from FOAF
        
        @param foaf: a foaf uri
        @param sha1mail: mail addess enconded
        @return: picture url        
        """
        
        graph = self.__getGraph(foaf)
        
        if (graph != None):
        
            sparqlGr = SPARQLGraph(graph)
            select = ('?pic')
            where  = GraphPattern([ ('?x', RDF['type'], FOAF['Person']),
                                    ('?x', FOAF['mbox_sha1sum'], sha1mail),
                                    ('?x', FOAF['depiction'], '?pic')   
                                  ])
        
            result = Query.query(sparqlGr, select, where)
        
            for one in result:
                return one
        
        return None
        

        
    def getShaMail(self, mail):
        """
        Services to obtain encrypted email address
        
        @param mail: an email address
        @type mail: string
        @return: encryted mail on foaf:mbox_sha1sum format
        @rtype: string
        """        
        
        return sha.new('mailto:'+mail).hexdigest()

