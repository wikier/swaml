#!/usr/bin/env python2.4

import sys
from SOAPpy import SOAPProxy

mbox = '119222cf3a2893a375cc4f884a0138155c771415'

host = '192.168.2.243'
port = '8880'
WS_NS = 'http://frade.no-ip.info/wsFOAF'

uri = None

try:

	remote = SOAPProxy(host+':'+port, namespace=WS_NS, soapaction='')
	uri = remote.getFoaf(mbox)

except Exception, detail:
	print 'Exception #' + str(detail[0]) + ' in Web Service: ' + detail[1]

if (uri != None):
	print mbox + ': ' + uri
else:
	print 'no foaf founded for ' + mbox
