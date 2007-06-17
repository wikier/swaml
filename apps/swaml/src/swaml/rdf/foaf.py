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
import rdflib
from rdflib.Graph import ConjunctiveGraph
from rdflib.sparql.sparqlGraph import SPARQLGraph
from rdflib.sparql.graphPattern import GraphPattern
from rdflib.sparql import Query
from rdflib import Namespace, Literal
from swaml.rdf.namespaces import SWAML, SIOC, RDF, RDFS, FOAF, GEO
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
        Services to obtain FOAF URI from an email sha1sum
        
        @param mail_sha1sum: an email address sha1sum
        @type mail_sha1sum: string
        @return: the FOAF URI of this email owner
        @rtype: string
        
        @todo: customize FOAF service
        """
        
        # TODO: customize this with a real service
        #
        #         ideas: - PyGoogle <http://pygoogle.sourceforge.net/> 
        #                      import google
        #                      google.LICENSE_KEY = '...'
        #                      data = google.doGoogleSearch('119222cf3a2893a375cc4f884a0138155c771415 filetype:rdf')
        #
        #                - Swoogle <http://swoogle.umbc.edu/>
        #
        #                -  Ping the Semantic Web.com <http://pingthesemanticweb.com/>
        
        foafs = {    'd0fd987214f56f70b4c47fb96795f348691f93ab' : 'http://www.wikier.org/foaf.rdf',
                     '119222cf3a2893a375cc4f884a0138155c771415' : 'http://www.wikier.org/foaf.rdf',
                     '98a99390f2fe9395041bddc41e933f50e59a5ecb' : 'http://www.berrueta.net/foaf.rdf',
                     '8114083efd55b6d18cae51f1591dd9906080ae89' : 'http://di002.edv.uniovi.es/~labra/labraFoaf.rdf',
                     '84d076726727b596b08198e26ef37e4817353e97' : 'http://frade.no-ip.info:2080/~ivan/foaf.rdf',
                     '3665f4f2370ddd6358da4062f3293f6dc7f39b7c' : 'http://eikeon.com/foaf.rdf',
                     '56e6f2903933a611708ebac456d45e454ddb8838' : 'http://captsolo.net/semweb/foaf-captsolo.rdf',
                     '42ec6894d9a48b5647279e866a0643eb7caded36' : 'http://captsolo.net/semweb/foaf-captsolo.rdf',
                     '9a6b7eefc08fd755d51dd9321aecfcc87992e9a2' : 'http://www.johnbreslin.com/foaf/foaf.rdf',
                     '36cf5b9757bdc1529831c210dbd81961472f1eb0' : 'http://platon.escet.urjc.es/~axel/foaf.rdf',
                     '80248cbb1109104d97aae884138a6afcda688bd2' : 'http://apassant.net/foaf.rdf',
                     '669fe353dbef63d12ba11f69ace8acbec1ac8b17' : 'http://dannyayers.com/misc/foaf/foaf.rdf',
                     '349f4bf50f11185d3503b14f1a6ccfc425116b12' : 'http://www.openlinksw.com/dataspace/kidehen@openlinksw.com/about.rdf',
                     'f67ba8825fc92f3db74ae725491c7c224287a367' : 'http://www.talkdigger.com/foaf/fgiasson'
                }
                
        if (mail_sha1sum in foafs):
            return foafs[mail_sha1sum]
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
