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

http://sindice.com/dev?section=api
"""

import urllib2

class Sindice:
    
    def __init__(self):
        self.service = "http://sindice.com/query/lookup?%s&format=txt" 
        
    def __request(self, uri):
        headers = { 'User-Agent' : "swaml (http://swaml.berlios.de/; sergio@wikier.org)" }
        request = urllib2.Request(uri)
        return urllib2.urlopen(request)
    
    def lookupURIs(self, uri):
        print "TODO"
    
    def lookupKeywords(self, keyword):
        print "TODO"
    
    def lookupIFPs(self, property, object):
        query = "property=%s&object=%s" % (property, object)
        uri = self.service % query
        response = self.__request(uri)
        results = []
        for line in response:
            line = line.split("\t")
            results.append((line[0], line[1]))
        return results
        
if __name__ == "__main__":
    #FIXME: only to test
    s = Sindice()
    results = s.lookupIFPs("http://xmlns.com/foaf/0.1/mbox_sha1sum", "d0fd987214f56f70b4c47fb96795f348691f93ab")
    for uri, date in results:
        print uri

    
    
