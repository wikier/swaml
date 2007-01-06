# SWAML <http://swaml.berlios.de/>
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

"""PingTheSemanticWeb.com wrapper"""

import urllib2

class PTSW:
    
    def __init__(self):
        self.rest = "http://pingthesemanticweb.com/rest/?url="
        self.pinged = 0

    def ping(self, uri):
        try:
            print 'ping', uri
            uri = uri.replace(":", "%3A")
            import socket
            socket.setdefaulttimeout(5)
            response = urllib2.urlopen(self.rest+uri).read()
            responseParsed = self.parseResponse(response)
            ok = (responseParsed['flerror'] == 0)
            if ok:
                self.pinged += 1
            return ok
        except:
            return False
        
    def parseResponse(self, response):
        dom = minidom.parseString(response)
        responses = dom.getElementsByTagName('response')
        dict = {}
        for node in responses[0].childNodes:
            if (not node.nodeType == node.TEXT_NODE):
                key = node.nodeName
                try:
                    value = int(node.firstChild.data)
                except:
                    value = node.firstChild.data
                dict[key] = value
                    
        return dict
    
    def stats(self):
        return self.pinged, 'SIOC files pinged'
