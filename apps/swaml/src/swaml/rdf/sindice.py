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
A python client for sindice.com

seeAlso: http://sindice.com/dev/api
"""

import urllib2

class Sindice:
    
    def __init__(self):
        """
        Sindice constructor     
        """
        
        self.service = "http://sindice.com/query/lookup?%s&format=txt" 
        
    def __request(self, uri):
        """
        Generic request
        
        @param uri: uri to request
        @return: response
        """
        
        headers = { 'User-Agent' : "swaml (http://swaml.berlios.de/; sergio@wikier.org)" }
        request = urllib2.Request(uri)
        return urllib2.urlopen(request)
    
    def lookupURIs(self, uri):
        """
        Lookup URIs
        
        @param uri: uri to query
        @return: results
        """
        
        print "TODO"
        return []
    
    def lookupKeywords(self, keyword):
        """
        Lookup keywords
        
        @param keyword: keyword to query
        @return: picture results
        """
        
        print "TODO"
        return []
    
    def lookupIFPs(self, property, object):
        """
        Lookup IFPs
        
        @param property: property to query
        @param object: object
        @return: results       
        """
        
        query = "property=%s&object=%s" % (property, object)
        uri = self.service % query
        response = self.__request(uri)
        results = []
        for line in response:
            line = line.split("\t")
            results.append((line[0], line[1]))
        return results
