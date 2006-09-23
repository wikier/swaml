#!/usr/bin/env python2.4

import sys
from SOAPpy import SOAPServer

WS_NS = 'http://frade.no-ip.info/wsFOAF'


class foafWS:
    def test(self):
        return "Cadena de prueba"

    def getFoaf(self, chain):
        return "http://www.wikier.org/foaf.rdf"


server = SOAPServer(('', 8880))
ws = foafWS()

server.registerObject(ws, WS_NS)

print "Starting server..."
server.serve_forever()
