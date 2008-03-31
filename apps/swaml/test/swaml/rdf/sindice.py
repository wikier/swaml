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

import unittest
from rdflib.Graph import ConjunctiveGraph
from rdflib.sparql.bison import Parse
import sys
sys.path.append("./src")
from swaml.rdf.sindice import Sindice
from swaml.rdf.namespaces import RDF, FOAF, NSbindings

class TestSindice(unittest.TestCase):

    def setUp(self):
        mbox = "d0fd987214f56f70b4c47fb96795f348691f93ab"
        s = Sindice()
        self.results = s.lookupIFPs("http://xmlns.com/foaf/0.1/mbox_sha1sum", mbox)

    def tearDown(self):
        self.results = None

    def testFirst(self):
        self.assertEquals(self.results[0][0], "http://www.wikier.org/foaf#me")

    def testQueryingMore(self):
        for result in self.results:
            uri = result[0]
            g = ConjunctiveGraph()
            g.parse(uri)
            query = Parse("""
                                SELECT ?person
                                WHERE {
                                         <%s> foaf:primaryTopic ?person .
                                         ?person rdf:type foaf:Person . 
                                      }
                          """ % uri )
            queryResults = g.query(query, initNs=NSbindings).serialize('python')
            if (len(queryResults)>0):
                self.assertEquals(str(queryResults[0]), "http://www.wikier.org/foaf#wikier")


if __name__ == "__main__":
    unittest.main()

