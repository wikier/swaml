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

"""Software to export SWAML's subscribers into KML"""

import sys, os, string
from classes.ui import CommandLineUI
import rdflib
from rdflib import sparql
from classes.namespaces import SWAML, SIOC, RDF, FOAF, GEO
from classes.kml import KML

class SwamlKmlExporter(CommandLineUI):
    """
    SWAML's subscribers exporter into KML
    
    @author: Sergio Fdez
    @license: GPL
    """
    
    def parse(self, path):
        graph = rdflib.Graph()
        graph.parse(path)
        return graph
    
    def process(self, input, output=None):
        if (output == None):
            output = '.'.join(input.split('.')[:-1]) + '.kml'
        
        graph = self.parse(input)
        
        #sparql query
        sparqlGr = sparql.sparqlGraph.SPARQLGraph(graph)
        select = ('?name', '?lat', '?lon', '?pic')
        where = sparql.GraphPattern(
            [('?x', RDF['type'], SIOC['User']),
             ('?x', SIOC['name'], '?name'),
             ('?x', FOAF['based_near'], "?y"),
             ('?y', GEO['long'], '?lon'),
             ('?y', GEO['lat'], '?lat')])
        opt = sparql.GraphPattern([('?x', SIOC['avatar'], "?pic")])
        users = sparqlGr.query(select, where, opt)
        
        n = len(users)
        if (n > 0):
            kml = KML()
            
            #create places
            for (name, lat, lon, pic) in users:
                kml.addPlace(lat, lon, str(name), pic)
                
            #and dump to disk
            try:
                kml_file = open(output, 'w+')
                kml.write(kml_file)
                kml_file.flush()
                kml_file.close()
                print 'new KML file created in', output, 'with', n, 'points'
            except IOError, detail:
                print 'Error exporting coordinates to KML: ' + str(detail)
                
        else:
            print 'Nobody with geographic information available in', input

    def __init__(self, argv):
        """
        main method
        @param argv: values of inline arguments
        """       
        
        CommandLineUI.__init__(self, 'kml')
        
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
        SwamlKmlExporter(sys.argv[1:])
    except KeyboardInterrupt:
        print 'Received Ctrl+C or another break signal. Exiting...'

                                                                            
del sys, os, string

