#!/usr/bin/env python2.4

import sys
from SOAPpy import SOAPProxy

foafs = {    'd0fd987214f56f70b4c47fb96795f348691f93ab' : 'http://www.wikier.org/foaf.rdf',
             '119222cf3a2893a375cc4f884a0138155c771415' : 'http://www.wikier.org/foaf.rdf',
             '98a99390f2fe9395041bddc41e933f50e59a5ecb' : 'http://www.berrueta.net/foaf.rdf',
             '8114083efd55b6d18cae51f1591dd9906080ae89' : 'http://di002.edv.uniovi.es/~labra/labraFoaf.rdf',
             '84d076726727b596b08198e26ef37e4817353e97' : 'http://frade.no-ip.info:2080/~ivan/foaf.rdf',
             '3665f4f2370ddd6358da4062f3293f6dc7f39b7c' : 'http://eikeon.com/foaf.rdf',
             '56e6f2903933a611708ebac456d45e454ddb8838' : 'http://captsolo.net/semweb/foaf-captsolo.rdf',
             '42ec6894d9a48b5647279e866a0643eb7caded36' : 'http://captsolo.net/semweb/foaf-captsolo.rdf',
             '9a6b7eefc08fd755d51dd9321aecfcc87992e9a2' : 'http://www.johnbreslin.com/foaf/foaf.rdf',
             '36cf5b9757bdc1529831c210dbd81961472f1eb0' : 'http://platon.escet.urjc.es/~axel/foaf.rdf',
             '80248cbb1109104d97aae884138a6afcda688bd2' : 'http://apassant.net/foaf.rdf',
             '669fe353dbef63d12ba11f69ace8acbec1ac8b17' : 'http://dannyayers.com/misc/foaf/foaf.rdf',
             '349f4bf50f11185d3503b14f1a6ccfc425116b12' : 'http://www.openlinksw.com/dataspace/kidehen@openlinksw.com/about.rdf',
             'f67ba8825fc92f3db74ae725491c7c224287a367' : 'http://www.talkdigger.com/foaf/fgiasson'
        }

host = '192.168.2.4'
port = '8880'
WS_NS = 'http://frade.no-ip.info/wsFOAF'

try:

	remote = SOAPProxy(host+':'+port, namespace=WS_NS, soapaction='')
	
	for hash in foafs.keys():
		print hash + ':',
		uri = remote.getFoaf(hash)
		if (uri == None):
			print 'not found'
		else:
			if (uri != foafs[hash]):
				print 'no:', foafs[hash], '-', uri
			else:
				print 'ok:', uri

except Exception, detail:
	print 'Exception #' + str(detail[0]) + ' in Web Service: ' + detail[1]

