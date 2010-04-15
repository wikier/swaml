# -*- coding: utf8 -*-

# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2005-2010 Sergio Fernández
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

"""Abstraction of a mailing list"""

import sys, os
import random
import datetime
from rdflib.Graph import ConjunctiveGraph
from rdflib import URIRef, Literal, BNode, RDF
from swaml.mail.mbox import Mbox
from swaml.rdf.sioc.subscribers import Subscribers
from swaml.rdf.sioc.message import Message
from swaml.rdf.sioc.index import Index
from swaml.rdf.namespaces import RDFS, SWAML, SIOC, SIOCT, FOAF, DC, MVCB
from swaml.common.date import FileDate
from shutil import copyfile

class MailingList:
    """
    Mailing List abstraction
    """
    
    def __init__(self, config, base="./", lang=None):
        """
        Constructor method
        
        @param config: configuration
        @param lang: language
        """
        
        self.config = config
        self.base = base
        self.lang = lang
        self.subscribers = Subscribers(config)
        self.index = Index(self.config)
        
        self.uri = self.config.get('base') + 'forum'
        
    def __createDir(self):
        """
        Create the necessary directory
        """
        
        if not (os.path.exists(self.config.get('dir'))):
            os.mkdir(self.config.get('dir'))
        
    def __parse(self):
        """
        Parse mailingg list and load all indexes into memory
        """
        
        previous = None
        
        mbox = Mbox(self.config.get('mbox'))
        messages = 0
        message = mbox.nextMessage()
        
        while(message != None):
            
            try:
                #fisrt load message
                msg = Message(message, self.config)
                
                #index it
                self.index.add(msg)
                self.subscribers.add(msg)
                subscriber = self.subscribers.get(msg.getFromMail())
                msg.setSender(subscriber)
                
                #parent message (refactor)
                inReplyTo = msg.getInReplyTo()
                if (inReplyTo != None):
                    parent = self.index.get(inReplyTo)
                    if (parent != None):
                        msg.setParent(parent) #link child with parent
                        parent.addChild(msg) #and parent with child
                        
                #and previous and next by date
                if (previous != None):
                    previous.setNextByDate(msg)
                    msg.setPreviousByDate(previous)
                
                previous = msg
            except KeyError, details:
                print 'Error parsing a mail form mailbox: ' + str(details)
            
    
            messages += 1
                        
            #and continue with next message
            message = mbox.nextMessage()

        self.messages = messages
    
    def publish(self):
        """
        Publish the messages
        """
        
        self.__createDir()
        
        #first lap
        self.__parse()
        
        #and second lap
        mbox = Mbox(self.config.get('mbox'))
        messages = 0

        message = mbox.nextMessage()
        
        while(message != None):
            
            try:
                messages += 1
                try:
                    id = message['Message-Id']
                except:
                    id = random.randint(1000000000, 9999999999) + "@localhost" #FIXME
                    print messages + "is not a valid RFC2822 message, it hasn't message-id field"
                msg = self.index.getMessage(messages)
                msg.setBody(message.fp.read())
                msg.toRDF()
                msg.toXHTML()
                #self.index.delete(id)
            except Exception, detail:
                print 'Error processing message ' + str(messages) + ': ' + str(detail)
                #import traceback
                #traceback.print_exc(file=sys.stdout)

            message = mbox.nextMessage()
            
        self.__toRDF()
        self.__toXHTML()
    
        if (self.config.get('foaf')):
            self.subscribers.process()
            
        self.subscribers.export()
            
        self.copyFiles()
            
        self.generateApacheConf()
                
        if (self.messages != messages):
            print 'Something was wrong: ' + str(self.messages) + ' parsed, but ' + str(messages) + ' processed'

        return messages
    
    def __getUri(self):
        """
        Get the mailing list URI
        
        @return: uri
        """
        
        return self.uri
    
    def __addSite(self, graph, url):
        """
        Add the site
        
        @param graph: mailing list graph
        @param url: site url
        @todo: write a new class
        """
        
        site = URIRef(url)
        graph.add((site, RDF.type, SIOC['Site']))
        graph.add((site, SIOC['host_of'], URIRef(self.__getUri())))
        
    
    def __toRDF(self):
        """
        Dump mailing list into a RDF file
        """

        #rdf graph
        store = ConjunctiveGraph()
        
        #namespaces
        store.bind('rdfs', RDFS)
        store.bind('swaml', SWAML)
        store.bind('sioc', SIOC)
        store.bind('sioct', SIOCT)
        store.bind('foaf', FOAF)
        store.bind('dc', DC)
        store.bind('mvcb', MVCB)

        #fisrt the host graph
        host = self.config.get('host')
        if (len(host) > 0):
            self.__addSite(store, host)

        #and then the mailing list
        list = URIRef(self.__getUri())
        store.add((list, RDF.type, SIOC['Forum']))
        #store.add((list, RDF.type, SIOCT['MailingList']))
        
        #list information
        title = self.config.get('title')
        if (len(title) > 0):
            store.add((list, DC['title'], Literal(title)))
            
        description = self.config.get('description')
        if (len(description) > 0):
            store.add((list, DC['description'], Literal(description)))
            
        if (len(host) > 0):
            store.add((list, SIOC['has_host'], URIRef(host)))
        
        store.add((list, SWAML['address'], Literal(self.config.get('to'))))
        store.add((list, DC['date'], Literal(FileDate(self.config.get('mbox')).getStringFormat())))
        store.add((list, MVCB['generatorAgent'], URIRef(self.config.getAgent())))
        store.add((list, MVCB['errorReportsTo'], URIRef('http://swaml.berlios.de/bugs')))
        if (self.lang != None):
            store.add((list, DC['language'], Literal(self.lang)))

        #subscribers
        subscribers = self.subscribers.getSubscribersUris()
        for uri in subscribers:
            store.add((list, SIOC['has_subscriber'], URIRef(uri)))
            store.add((URIRef(uri), RDF['type'], SIOC['UserAccount']))
                  
        #and all messages uris
        uris = self.index.getMessagesUri()                        
        for uri in uris:
            store.add((list, SIOC['container_of'], URIRef(uri)))
            store.add((URIRef(uri), RDF['type'], SIOC['Post']))
            parent = msg.getParent()
            if (parent != None):
                store.add((URIRef(uri), SIOC['reply_of'], URIRef[parent]))
                    
        #and dump to disk
        try:
            rdf_file = open(self.config.get('dir')+'forum.rdf', 'w+')
            rdf_file.write(store.serialize(format="pretty-xml"))
            rdf_file.flush()
            rdf_file.close()
        except IOError, detail:
            print 'Error exporting mailing list to RDF: ' + str(detail)
            
    def __toXHTML(self):
        pass
            
    def copyFiles(self):
        """
        Copy necessary files
        """
        
        copyfile(self.base + 'includes/ui/web/swaml.css', self.config.get('dir')+'swaml.css')
        
    def generateApacheConf(self):
        """
        Generate a customized htaccess file
        """
        
        #read template
        data = ''
        try:
            file = open(self.base + '.includes/apache/htaccess-files.tpl')
            for line in file:
                data += line
            file.close()
        except:
            print 'An exception occured reading apache template file'
            
        base = self.config.get('base')
        base = '/' + '/'.join(base.split('/')[3:])
        data = data.replace('{BASE}', base)
        
        #post/([0-9]{4}\-[A-Za-z]+/[0-9]+)$
        #RewriteRule ^post/([0-9]{4})-([A-Za-z]+)/([0-9]+)$ $1-$2/post-$3.xhtml [R=303]
        
        pattern = self.config.get('post')
        pattern = pattern.replace('DD', '[0-9]{2}')
        pattern = pattern.replace('MMMM', '[A-Za-z]{4}')
        pattern = pattern.replace('MMM', '[A-Za-z]{3}')
        pattern = pattern.replace('MM', '[0-9]{2}')
        pattern = pattern.replace('YYYY', '[0-9]{4}')
        pattern = pattern.replace('ID', '[0-9]+')
        pattern = pattern.replace('-', '\-')
        
        data = data.replace('{POSTURI}', '('+pattern+')')
        data = data.replace('{POSTFILE}', '$1')
        
        #and dump to disk
        try:
            file = open(self.config.get('dir')+'.htaccess', 'w+')
            file.write(data)
            file.flush()
            file.close()        
        except IOError, detail:
            print 'IOError saving message .htaccess file'
       
        
