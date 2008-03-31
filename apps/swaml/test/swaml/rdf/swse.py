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
import sys
sys.path.append("./src")
from swaml.rdf.swse import SWSE

class TestSWSE(unittest.TestCase):

    def testSergio(self):
        query = """
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    SELECT DISTINCT ?person
                    WHERE {
                      ?file foaf:primaryTopic ?person .
                      ?person rdf:type foaf:Person . 
                      ?person foaf:mbox_sha1sum "d0fd987214f56f70b4c47fb96795f348691f93ab"                                    
                    }
                """

        swse = SWSE()
        results = swse.query(query)

        self.assertTrue(len(results)>0)
        self.assertEquals(results[0], "http://www.wikier.org/foaf#wikier")


if __name__ == "__main__":
    unittest.main()

    
