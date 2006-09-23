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

import sys, os, string, sha
import rdflib
from rdflib.sparql import sparqlGraph, GraphPattern
from rdflib import Namespace, Literal
from namespaces import SWAML, RDF, RDFS, FOAF, GEO
from email.Header import decode_header
import email.Utils



class FoafUtils:
    """
    Collection of util services to SWAML
    """
    
    def __init__(self):
        self.__actualFoaf = None
        self.__graph = None
    
    def getFoaf(self, mail):
        """
        Services to obtain FOAF URI from an email address
        
        @param mail: an email address
        @type mail: string
        @return: the FOAF URI of this email owner
        @rtype: string
        
        @todo customize foaf service
        """
        
        mail_sha1sum = self.getShaMail(mail)
        
        # TODO: customize this with a real service
        #
        #         ideas: - PyGoogle <http://pygoogle.sourceforge.net/> 
        #                      import google
        #                      google.LICENSE_KEY = '...'
        #                      data = google.doGoogleSearch('119222cf3a2893a375cc4f884a0138155c771415 filetype:rdf')
        #
        #                - Swoogle <http://swoogle.umbc.edu/>
        #
        #                -  Ping the Semantic Web.com <http://pingthesemanticweb.com/>
        
        foafs = {    '119222cf3a2893a375cc4f884a0138155c771415' : 'http://www.wikier.org/foaf.rdf',
                     '98a99390f2fe9395041bddc41e933f50e59a5ecb' : 'http://www.asturlinux.org/~berrueta/foaf.rdf',
                     '8114083efd55b6d18cae51f1591dd9906080ae89' : 'http://di002.edv.uniovi.es/~labra/labraFoaf.rdf',
                     '84d076726727b596b08198e26ef37e4817353e97' : 'http://frade.no-ip.info:2080/~ivan/foaf.rdf',
                     'bd6566af7b3bfa28f917aa545bf4174661817d79' : 'http://www.asturlinux.org/~jsmanrique/foaf.rdf',
                     '97d9756f1281858d0e9e4489003073e4986546ce' : 'http://xtrasgu.asturlinux.org/descargas/foaf.rdf'
                }
                
        if (mail_sha1sum in foafs):
            return foafs[mail_sha1sum]
        else:
            return None
        
    def __getGraph(self, foaf):
        """
        A simple mechanism to cache foaf graph
        """
        
        #tip to set socket timeout global var
        import socket
        socket.setdefaulttimeout(10) #timeout in seconds
        
        if (self.__actualFoaf != foaf or self.__graph == None):
            self.__actualFoaf = foaf
            self.__graph = sparqlGraph.SPARQLGraph()
            try:
                self.__graph.parse(foaf)
            except:
                self.__graph = None
        
        return self.__graph
        
    def getGeoPosition(self, foaf, mail):
        """
        Obtain geography information from foaf
        """
        
        sparqlGr = self.__getGraph(foaf)
        
        if (sparqlGr != None):
        
            select = ('?lat', '?long')
            where  = GraphPattern([ ('?x', RDF['type'], FOAF['Person']),
                                    ('?x', FOAF['mbox_sha1sum'], self.getShaMail(mail)),
                                    ('?x', FOAF['based_near'], '?y'),
                                    ('?y', GEO['lat'], '?lat'),
                                    ('?y', GEO['long'], '?long')    
                                  ])
        
            result = sparqlGr.query(select, where)
        
            for one in result:
                return [one[0], one[1]]
        
        return [None, None]
    
    def getPic(self, foaf, mail):
        """
        Get picture from FOAF
        """
        sparqlGr = self.__getGraph(foaf)
        
        if (sparqlGr != None):
        
            select = ('?pic')
            where  = GraphPattern([ ('?x', RDF['type'], FOAF['Person']),
                                    ('?x', FOAF['mbox_sha1sum'], self.getShaMail(mail)),
                                    ('?x', FOAF['depiction'], '?pic')   
                                  ])
        
            result = sparqlGr.query(select, where)
        
            for one in result:
                return one
        
        return None
        

        
    def getShaMail(self, mail):
        """
        Services to obtain encrypted email address
        
        @param mail: an email address
        @type mail: string
        @return: encryted mail on foaf:mbox_sha1sum format
        @rtype: string
        """        
        
        return sha.new('mailto:'+mail).hexdigest()


class Charset:
    """
    Collection of services related with charset and encondig
    """
    
    def __init__(self, charset='iso-8859-1'):
        self.charset = charset
    
    def encode(self, orig):
        """
        Decode an string
        """
        
        ret = ''
        
        try:
            ret = self.__force_decode(orig)
        except Exception:
            ret = self.__unicode(orig, self.charset)
            
        return ret
            
    def __decode(self, orig):            
        #tip because decode_header returns the exception 
        #    ValueError: too many values to unpack
        #TODO: performance this tip
        parted = orig.split(' ') 
        dest = ''
        for one in parted:
            [(s, enconding)] = decode_header(one)
            if (dest == ''):
                dest = s
            else:
                dest += ' ' + s
        
        return dest
    
    def __unicode(self, orig, charset):
        ret = ''
        
        try:
            ret = unicode(orig, charset)
        except TypeError:
            ret = orig   
                     
        return orig
        
    

class DateUtils:
    
    def __init__(self, date):
        self.date = email.Utils.parsedate(date)
    
    def getDay(self):
        return self.date[2]
    
    def getStringDay(self):
        day = self.getDay()
        if (day < 10):
            return ('0' + str(day))
        else:
            return str(day)
        
    def getMonth(self):
        return self.date[1]
    
    def getStringMonth(self):
        month = self.getMonth()
        if (month < 10):
            return ('0' + str(month))
        else:
            return str(month)
    
    def getShortStringMonth(self):
        shortMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return shortMonths[self.getMonth() - 1]
        
    def getLongStringMonth(self):
        longMonths = ['January', 'February', 'March', 'April', 
                       'May', 'June', 'July', 'August', 
                       'September', 'October', 'November', 'December']
        return longMonths[self.getMonth() - 1]  
    
    def getYear(self):
        return self.date[0]
    
    def getStringYear(self):
        return str(self.getYear())
    
    def getNumericFormat(self):
        return [self.getYear(), self.getMonth(), self.getDay()]  
    
    def getStringFormat(self, format='iso'):  
        year, month, day = self.getNumericFormat()
        
        if(format == 'normal'):
            #normal format: day-month-year
            return str(day) + '-' + str(month) + '-' + str(year)
        else:
            #iso: year-month-day
            return str(year) + '-' + str(month) + '-' + str(day)
            
        
