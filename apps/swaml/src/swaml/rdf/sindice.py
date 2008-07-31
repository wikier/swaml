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
A python client for Sindice.com

See also: http://sindice.com/developers/api
"""

import urllib
import urllib2
import simplejson
import warnings

class Sindice:
    
    def __init__(self):
        """
        Sindice constructor     
        """
        
        self.service1 = "http://sindice.com/query/v1/lookup?%s&format=txt"
        self.service2 = "http://api.sindice.com/v2/search?q=%s&qt=%s" 
        
    def __request(self, uri, accept="application/json"):
        """
        Generic request
        
        @param uri: uri to request
        @return: response
		@rtype: file-like object
        """
        
        headers = { 
                    "User-Agent" : "swaml (http://swaml.berlios.de/; sergio@wikier.org)",
                    "Accept"     : accept
                  }
        request = urllib2.Request(uri, headers=headers)
        return urllib2.urlopen(request)
    
    def lookupURIs(self, uri):
        """
        Lookup URIs
        
        @param uri: uri to query
        @return: results
		@rtype: list
        """

        warnings.warn("This method is deprecated becuase it uses the old Sindice's API", DeprecationWarning, stacklevel=3) 
        
        print "TODO"
        return []
    
    def lookupKeywords(self, keyword):
        """
        Lookup keywords
        
        @param keyword: keyword to query
        @return: picture results
		@rtype: list
        """

        warnings.warn("This method is deprecated becuase it uses the old Sindice's API", DeprecationWarning, stacklevel=3)
        
        print "TODO"
        return []
    
    def lookupIFPs(self, property, object):
        """
        Lookup IFPs
        
        @param property: property to query
        @param object: object
        @return: results
        @rtype: list   
        """

        warnings.warn("This method is deprecated becuase it uses the old Sindice's API", DeprecationWarning, stacklevel=3)
        
        query = "property=%s&object=%s" % (property, object)
        uri = self.service1 % query
        response = self.__request(uri, accept="text/plain")
        results = []
        for line in response:
            line = line.split("\t")
            results.append((line[0], line[1]))
        return results

    def query(self, query, qt="term"):
        """
        An advanced query

        @param triple: triple/s to query
        @return: results
        @rtype: list
        """

        uri = self.service2 % (urllib.quote(query), qt)
        response = self.__request(uri)
        results = []
        json = simplejson.load(response)
        for entry in json["entries"]:
            link = entry["link"]
            if not link in results:
                results.append(link)
        return results

    def sparql(self, query):
        """
        A SPARQL translator
        """

        print "TODO"
        return []

