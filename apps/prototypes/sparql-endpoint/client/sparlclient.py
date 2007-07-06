#!/usr/bin/env python2.4
#
# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2007 Sergio Fdez, Diego Berrueta
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

"""A basic SPARQL client"""

import sys
import urllib, urllib2
from rdflib.Graph import ConjunctiveGraph
from rdflib.StringInputSource import StringInputSource


class SPARQLClient:
    
    def __init__(self, server, serialization='application/rdf+xml'):
        """
        Client constructor
        
        @param server: sparql end-point server url
        @param serialization: results serialization (see http://www.openrdf.org/doc/sesame2/system/ch08.html#table-var-binding-formats)
        """        
        self.server = server
        self.serialization = serialization
    
    def query(self, type, query, lang='sparql'):
        """
        SPARQL query
        
        @todo: implement select query
        
        @param type: query type (CONSTRUCT or SELECT)
        @param query: text query
        @param lang: query lang (SPARQL or SeRQL)
        @return: graph with query result
        """        
        
        url =  self.server
        data = { 'query' : query, 'queryLn' : lang.lower() }
        params = urllib.urlencode(data)  
        
        try:
            headers = { 'Accept': self.serialization, 'User-Agent' : 'SWAML SPARQLClient' }
            request = urllib2.Request(url, params, headers)
            result = urllib2.urlopen(request).read()
        except urllib2.HTTPError, e:
            result = urllib2.urlopen(url, params).read()        
        
        graph = self.parse(result)
        return graph
        

    def parse(self, result):
        """
        Parse query result
        
        @param result: text result
        @return: rdf graph
        """        
        graph = ConjunctiveGraph()
        graph.parse(StringInputSource(result))
        return graph


if __name__ == '__main__':
    #lib demo
    try:
        server = 'http://wopr:8180/openrdf-http-server-2.0-beta5/repositories/prueba'
        query = 'CONSTRUCT {<http://swaml.berlios.de/demos/sioc-dev/2007-Feb/post-500.rdf> ?y ?z } WHERE { <http://swaml.berlios.de/demos/sioc-dev/2007-Feb/post-500.rdf> ?y ?z }'
        client = SPARQLClient(server)
        graph = client.query('CONSTRUCT', query)
        for x in graph.objects():
            print x
    except KeyboardInterrupt:
        print 'Received Ctrl+C or another break signal. Exiting...'
        