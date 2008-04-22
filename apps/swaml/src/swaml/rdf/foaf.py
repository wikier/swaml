# -*- coding: utf8 -*-

# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2005-2008 Sergio Fernández
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
from rdflib.sparql.bison import Parse
from rdflib import Namespace, Literal
from swaml.rdf.namespaces import SIOC, RDF, RDFS, FOAF, GEO, NSbindings
from swaml.rdf.sindice import Sindice
from swaml.rdf.swse import SWSE
from email.Header import decode_header

class FOAFS:
    """
    Collection of util services to SWAML
    """
    
    def __init__(self, config=None):
        """
        FOAF services constructor
        """
        
        self.__actualDoc = None
        self.__graph = None
        self.config = config
    
    def getFoaf(self, mail):
        """
        Services to obtain FOAF URI from an email address
        
        @param mail: an email address
        @type mail: string
        @return: the FOAF file and his FOAF URI of this email owner
        @rtype: tuple
        """
        
        mail_sha1sum = self.getShaMail(mail)
        return self.getFoafFromSha(mail_sha1sum)
        
    def getFoafFromSha(self, mail_sha1sum):
        """
        Obtain FOAF URI from an email sha1sum, provided by a external service
        
        @param mail_sha1sum: an email address sha1sum
        @type mail_sha1sum: string
        @return: the document and his FOAF URI of this coded email owner
        @rtype: tuple
        """

        if (self.config != None and self.config.get('search').lower() == 'sindice'):
            return self.getFoafWithSindice(mail_sha1sum)
        else:
            return self.getFoafWithSWSE(mail_sha1sum)
        
    def getFoafWithSindice(self, mail_sha1sum):
        """
        Obtain FOAF URI from an email sha1sum, provided by sindice.com
        
        @param mail_sha1sum: an email address sha1sum
        @type mail_sha1sum: string
        @return: the document and his FOAF URI of this coded email owner
        @rtype: tuple
        """

        s = Sindice()
        results = s.lookupIFPs("http://xmlns.com/foaf/0.1/mbox_sha1sum", mail_sha1sum)
        return self.__getBestURI(results)

    def getFoafWithSWSE(self, mail_sha1sum):
        """
        Obtain FOAF URI from an email sha1sum, provided by swse.deri.org
        
        @param mail_sha1sum: an email address sha1sum
        @type mail_sha1sum: string
        @return: the document and his FOAF URI of this coded email owner
        @rtype: tuple
        """
        
        query = """
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    SELECT DISTINCT ?file ?person
                            ?file foaf:primaryTopic ?person .
                            ?person rdf:type foaf:Person . 
                            ?person foaf:mbox_sha1sum "%s"                                    
                          }
                """

        swse = SWSE()
        results = swse.query(query % mail_sha1sum)
        if len(results) > 0:
            return (results[0]['file'], results[0]['person'])
        else:
            query2 = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                        SELECT DISTINCT ?file ?person
                        WHERE { 
                                ?person rdf:type foaf:Person . 
                                ?person foaf:mbox_sha1sum "%s" .
                                ?person rdfs:seeAlso ?file                                  
                              }
                    """
            results2 = swse.query(query2 % mail_sha1sum)
            if len(results2) > 0:
                return (results2[0]['file'], results2[0]['person'])
            else:
                return (None, None)
    
    def __getBestURI(self, possibilities):
        """
        Search the file where a Person is the primary topic, else the first possibility

        @param possibilities: all the urls to choose
        @type possibilities: list of tuples
        @return better uri for a Person
        @rtype: string
        """
        for possibility in possibilities:
            doc = possibility[0]
            try:
                g = ConjunctiveGraph()
                g.parse(doc)
                #query = Parse("""
                #                SELECT ?person
                #                WHERE {
                #                        <%s> foaf:primaryTopic ?person .
                #                        ?person rdf:type foaf:Person .  
                #                        ?person foaf:mbox_sha1sum "%s"@en
                #                      }
                #              """ % (doc, mbox) )
                query = Parse("""
                                SELECT ?person
                                WHERE {
                                        <%s> foaf:primaryTopic ?person .
                                        ?person rdf:type foaf:Person .                                       
                                      }
                             """ % doc )
                queryResults = g.query(query, initNs=NSbindings).serialize('python')
                if len(queryResults) > 0 :
                    return (doc, queryResults[0])

            except Exception, details:
                print details

        if (len(possibilities)>0):
            return (possibilities[0][0], None)
        else:
            return (None, None)
        
    def __getGraph(self, doc):
        """
        A simple mechanism to cache foaf graph
        
        @param foaf: a foaf uri
        @return: the graph with the foaf loaded
        @rtype: rdflib.Graph.ConjunctiveGraph
        """
        
        #tip to set socket timeout global var
        import socket
        socket.setdefaulttimeout(10) #timeout in seconds
        
        if (self.__actualDoc != doc or self.__graph == None):
            self.__actualDoc = doc
            self.__graph = ConjunctiveGraph()
            try:
                self.__graph.parse(doc)
            except:
                self.__graph = None
        
        return self.__graph
        
    def getGeoPosition(self, foaf, doc, sha1mail):
        """
        Obtain geography information from foaf
        
        @param foaf: person uri
        @param doc: document that contains that person
        @param sha1mail: mail addess enconded
        @return: coordinates      
        """
        
        if (doc != None):
            graph = self.__getGraph(doc)
        
            if (graph != None):
                    query = """
                                SELECT ?lat ?lon
                                WHERE {
                                        <%s> rdf:type foaf:Person .
                                        <%s> foaf:based_near ?point .
                                        ?point rdf:type geo:Point .
                                        ?point geo:lat ?lat .
                                        ?point geo:long ?lon                                      
                                       }
                             """ % (foaf,foaf)
                    results = graph.query(Parse(query), initNs=NSbindings).serialize('python')
                    if len(results) > 0 :
                        return (results[0][0], results[0][1])
                    else:
                        query2 = """
                                    SELECT ?lat ?lon
                                    WHERE {
                                            ?person rdf:type foaf:Person .
                                            ?person foaf:mbox_sha1sum "%s"@en .
                                            ?person foaf:based_near ?point .
                                            ?point rdf:type geo:Point .
                                            ?point geo:lat ?lat .
                                            ?point geo:long ?lon .                                      
                                          }
                                """ % sha1mail
                        results2 = graph.query(Parse(query2), initNs=NSbindings).serialize('python')
                        if len(results2) > 0 :
                            return (results2[0][0], results2[0][1])
        
        return (None, None)
    
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

        mail = mail.lower() # I'm no sure if it's a good idea...
        return sha.new('mailto:'+mail).hexdigest()

