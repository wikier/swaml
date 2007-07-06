#!/usr/bin/env python2.4

import sys
import urllib, urllib2
from rdflib.Graph import ConjunctiveGraph
from rdflib.StringInputSource import StringInputSource


class SPARQLClient:
    
    def __init__(self, server, serialization='application/rdf+xml'):
        self.server = server
        self.serialization = serialization
    
    def query(self, query, lang='sparql'):
        
        url =  self.server
        data = {'query' : query, 'queryLn' : lang}
        params = urllib.urlencode(data)  
        
        try:
            
            headers = {'Accept': self.serialization, 'User-Agent' : 'SPARQLClient'}
            request = urllib2.Request(url, params, headers)
            result = urllib2.urlopen(request).read()
        except urllib2.HTTPError, e:
            result = urllib2.urlopen(url, params).read()        
        
        graph = self.parse(StringInputSource(result))
        return graph
        

    def parse(self, result):
        graph = ConjunctiveGraph()
        graph.parse(result)
        return graph


if __name__ == '__main__':
    #lib demo
    try:
        server = 'http://wopr:8180/openrdf-http-server-2.0-beta5/repositories/prueba'
        query = 'CONSTRUCT {<http://swaml.berlios.de/demos/sioc-dev/2007-Feb/post-500.rdf> ?y ?z } WHERE { <http://swaml.berlios.de/demos/sioc-dev/2007-Feb/post-500.rdf> ?y ?z }'
        client = SPARQLClient(server)
        graph = client.query(query)
        for x in graph.objects():
            print x
    except KeyboardInterrupt:
        print 'Received Ctrl+C or another break signal. Exiting...'
        