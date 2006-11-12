#!/usr/bin/env python2.4
# -*- coding: utf8 -*-
#
# SWAML KML Exporter <http://swaml.berlios.de/>
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

"""Software to enrich SWAML's subscribers using FOAF"""

import sys, os, string
from classes.ui import CommandLineUI
import rdflib
from rdflib import sparql, BNode, Literal, URIRef
from classes.namespaces import SWAML, SIOC, RDF, FOAF, GEO, RDFS
from classes.services import FoafUtils

class SwamlFoafEnricher(CommandLineUI):
    """
    SWAML's subscribers enricher with FOAF
    
    @author: Sergio Fdez
    @license: GPL
    """
    
    def parse(self, path):
        graph = rdflib.Graph()
        graph.parse(path)
        return graph
    
    def enriched(self, graph):
        
        sparqlGr = sparql.sparqlGraph.SPARQLGraph(graph)
        select = ('?foaf')
        where = sparql.GraphPattern(
                                     [('?user', RDF['type'], SIOC['User']),
                                      ('?user', RDFS['seeAlso'], '?foaf')])
        foafs = sparqlGr.query(select, where)
        
        return (len(foafs) > 0)
    
    def process(self, input, output=None):
        
        graph = self.parse(input)
        
        if not self.enriched(graph):
            
            if (output == None):
                output = '.'.join(input.split('.')[:-1]) + '.foaf.enrichment.rdf'
            
            #sparql query
            sparqlGr = sparql.sparqlGraph.SPARQLGraph(graph)
            select = ('?user', '?email_sha1sum')
            where = sparql.GraphPattern(
                [('?user', RDF['type'], SIOC['User']),
                 ('?user', SIOC['email_sha1sum'], '?email_sha1sum')])
            users = sparqlGr.query(select, where)
            
            if (len(users) > 0):
                foafserv = FoafUtils()
                n = 0
                
                graph.bind('foaf', FOAF)
                graph.bind('sioc', SIOC)
                graph.bind('geo', GEO)
                graph.bind('rdfs', RDFS)
                
                for (user, email_sha1sum) in users:
                    foaf = foafserv.getFoafFromSha(email_sha1sum)
                    if (foaf != None):
                        n += 1
                        
                        graph.add((user, RDFS['seeAlso'], URIRef(foaf)))
                        
                        lat, lon = foafserv.getGeoPosition(foaf, email_sha1sum)
                        if (lat != None and lon != None):                        
                            geo = BNode()
                            graph.add((user, FOAF['based_near'], geo))
                            graph.add((geo, RDF.type, GEO['Point']))        
                            graph.add((geo, GEO['lat'], Literal(lat)))
                            graph.add((geo, GEO['long'], Literal(lon)))
                    
                        pic = foafserv.getPic(foaf, email_sha1sum)
                        if (pic != None):
                            graph.add((user, SIOC['avatar'], URIRef(pic)))
    
                        
                #and dump to disk
                try:
                    rdf_file = open(output, 'w+')
                    graph.serialize(destination=rdf_file, format="pretty-xml")
                    rdf_file.flush()
                    rdf_file.close()
                    print 'new subscriber RDF file created in', output, 'enriched with', n, 'FOAF files'
                except IOError, detail:
                    print 'Error exporting subscriber to RDF: ' + str(detail)
                    
            else:
                print 'Nobody with FOAF description available in', input
                
        else:
            print input, 'is already enriched with FOAF'
        
    def __init__(self, argv):
        """
        main method
        @param argv: values of inline arguments
        """       
        
        CommandLineUI.__init__(self, 'foaf')
        
        for arg in argv:
            if arg == "-h" or arg == "--help":
                self.usage()
                
        
        if (len(argv)>=1):
            input = argv[0]
            if (len(argv)>1):
                output = argv[1]
            
            if (os.path.exists(input)):
                self.process(input, output)
            else:
                print input, 'is not a valid path'
        else:
            self.usage()


if __name__ == '__main__':
    try:
        SwamlFoafEnricher(sys.argv[1:])
    except KeyboardInterrupt:
        print 'Received Ctrl+C or another break signal. Exiting...'

                                                                            
del sys, os, string

