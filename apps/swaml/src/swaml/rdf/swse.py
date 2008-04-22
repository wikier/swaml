# -*- coding: utf8 -*-

# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2008 Sergio Fernández
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

"""
A simple python wrapper for SWSE

seeAlso: http://swse.deri.org/
"""

from SPARQLWrapper import SPARQLWrapper, JSON

class SWSE:
    
    def __init__(self):
        """
        SWSE constructor     
        """
        
        self.service = "http://swse.deri.org/yars2/query"

    def query(self, query):
        """
        SWSE Query
        
        @param query: sparql query
        @return: results       
        """

        queryResults = []        

        try:
            sparql = SPARQLWrapper(self.service)
            #sparql = SPARQLWrapper(self.service, agent="swaml (http://swaml.berlios.de/; sergio@wikier.org)")
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            if results.has_key("results"):
                results = results["results"]["bindings"] 
                for result in results:
                    if (len(result.keys()) == 1):
                        queryResults.append(result[result.keys()[0]]['value'])
                    else:
                        one = {}
                        for key in result.keys():
                            one[key] = result[key]['value']
                        queryResults.append(one)
        except Exception:
            print "Exception calling SWSE" #FIXME
        
        return queryResults

