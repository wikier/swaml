# -*- coding: utf8 -*-

# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2005-2007 Sergio Fernández, Diego Berrueta
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

"""Mail message abstraction"""

import sys, os, string, sha
import datetime, email, email.Errors
from rdflib.Graph import ConjunctiveGraph
from rdflib import URIRef, Literal, BNode
from rdflib import RDF
from swaml.rdf.namespaces import SIOC, RDFS, FOAF, DC, DCT, MVCB, XSD
from swaml.common.charset import Charset, fixCodification
from swaml.common.date import MailDate, FileDate
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation, DocumentType

class Message:
    """
    Mail message abstraction
    """
    
    id = 0
    
    def __init__(self, msg, config, sender=None):
        """
        Message constructor
        
        @param msg: plain message object
        @param config: configuration reference
        @param sender: author message reference
        """
        
        self.__class__.id += 1
        self.id = self.__class__.id
        self.config = config
        self.sender = sender
        self.subject = msg['Subject']
        self.messageId = msg['Message-Id']
        self.date = msg['Date']
        self.From = msg['From']
        self.getAddressFrom = msg.getaddr('From')
	
        try:
            self.to = msg['To']    
        except:
            #some mails have not a 'to' field
            self.to = self.config.get('to')   
            
        try:
            self.inReplyTo = msg['In-Reply-To']    
        except:
            self.inReplyTo = None
            
        self.parent = None
        self.childs = []
            
        self.__calculateId()
        self.nextByDate = None
        self.previousByDate = None

        #Obtain message path        
        #FIXME: format permited vars (feature #1355)
        index = self.config.get('post')
        
        #message date
        date = MailDate(self.date)   
             
         #replace vars
        index = index.replace('DD', date.getStringDay()) #day
        index = index.replace('MMMM', date.getLongStringMonth()) #long string month
        index = index.replace('MMM', date.getShortStringMonth()) #short string month
        index = index.replace('MM', date.getStringMonth()) #numeric month
        index = index.replace('YYYY', date.getStringYear()) #year
        index = index.replace('ID', str(self.id)) #swaml id

        #create subdirs
        dirs = index.split('/')[:-1]
        index_dir = ''
        for one_dir in dirs:
            index_dir += one_dir + '/'
            if not (os.path.exists(self.config.get('dir')+index_dir)):
                os.mkdir(self.config.get('dir')+index_dir)
                
        self.dir = index_dir
        self.path = index
        
        self.uri = self.config.get('base') + self.path
        
        #body after indexing all messages
        self.body = msg.fp.read()
        #[(self.body, enconding)] = decode_header(msg.fp.read())
        
    def setBody(self, body):
        """
        Set body content
        
        @param body: content
        """
        
        try:
            self.body = unicode(body) #fixCodification(body)
        except:
            self.body = ""
        
    def setSender(self, sender):
        """
        Set message's sender
        
        @param sender: author
        """
        
        self.sender = sender
        
    def setParent(self, parent):
        """
        Set parent message
        
        @param parent: parent reference
        """
        
        self.parent = parent.getUri()
        
    def addChild(self, child):
        """
        Add new child message
        
        @param child: child reference
        """
        
        self.childs.append(child.getUri())
        
    def setNextByDate(self, next):
        """
        Set next message by date
        
        @param next: next message reference
        """
        
        self.nextByDate = next.getUri()
        
    def setPreviousByDate(self, previous):
        """
        Set previous message by date
        
        @param previous: previous message reference
        """
                
        self.previousByDate = previous.getUri()
        
    def getId(self):
        """
        Get message ID
        
        @return: id
        """
        
        return self.id
    
    def getSwamlId(self):
        """
        Get message SWAML ID
        
        @return: swaml id
        """
        
        return self.swamlId    
    
    def getMessageId(self):
        """
        Get message ID field
        
        @return: id field
        """
        
        return self.messageId
    
    def getUri(self):    
        """
        Get message URI
        
        @return: uri
        """
        
        return self.uri
    
    def getRdfPath(self):
        return self.config.get('dir') + self.path + '.rdf'

    def getRdfUrl(self):
        return self.getUri() + '.rdf'
        
    def getXhtmlPath(self):
        return self.config.get('dir') + self.path + '.html'

    def getXhtmlUrl(self):
        return self.getUri() + '.html'
    
    def getSender(self):
        """
        Get message sender
        
        @return: author
        """
        
        return self.sender
    
    def __parseFrom(self, from_text):
        """
        Method to parse from field
        
        @param from_text: from field
        """
        
        from_parted = from_text.split(' ')
        name = ' '.join(from_parted[:-1])
        mail = from_parted[-1]

        return [name, mail]
    
    def getFromName(self):   
        """
        Get message from name
        
        @return: name
        """     
           
        if(self.From.find('<')!= -1):
            #mail similar than: Name Surmane <name@domain.com>
            from_name = str(self.getAddressFrom[0])
        else:
            #something like: Name Surmane name@domain.com
            from_name, from_mail = self.__parseFrom(self.From)
            
        return Charset().encode(from_name)
            
    def getFromMail(self):
        """
        Get from mail
        
        @return: mail
        """
        
        if(self.From.find('<')!= -1):
            #mail similar than: Name Surmane <name@domain.com>
            return str(self.getAddressFrom[1])
        else:
            #something like: Name Surmane name@domain.com
            from_name, from_mail = self.__parseFrom(self.From)
            return from_mail             
        
        
    def getTo(self):
        """
        Get To field
        
        @return: to
        """
                        
        to = self.to
                
        to = to.replace('@', self.config.getAntiSpam())
        to = to.replace('<', '')
        to = to.replace('>', '')                                     
        
        return to
    
    def getSubject(self):
        """
        Get subject
        
        @return: subject
        """        
        
        return Charset().encode(self.subject)
        
    def getDate(self):
        """
        Get date
        
        @return: date string
        """
                
        return self.date
    
    def getInReplyTo(self):
        """
        Get in-reply-to field
        
        @return: in-reply-to
        """
        
        return self.inReplyTo
    
    def getParent(self):
        """
        Get parent message
        
        @return: parent
        """
        
        return self.parent
    
    def getNextByDate(self):
        """
        Get next message by date
        
        @return: next
        """
        return self.nextByDate
        
    def getPreviousByDate(self):
        """
        Get previous message by date
        
        @return: previous
        """
        
        return self.previousByDate
   
    def getBody(self):
        """
        Get message body content
        
        @return: body
        """
        
        return self.body
    
    def toRDF(self):
        """
        Print a message into RDF in XML format
        """
        
        #rdf graph
        store = ConjunctiveGraph()
        
        #namespaces        
        store.bind('sioc', SIOC)
        store.bind('foaf', FOAF)
        store.bind('rdfs', RDFS)
        store.bind('dc', DC)
        store.bind('dct', DCT)

        #message node
        message = URIRef(self.getUri())
        store.add((message, RDF.type, SIOC["Post"]))

        #document node
        doc = URIRef(self.getUri()+'.rdf')
        store.add((doc, RDF.type, FOAF["Document"]))
        store.add((doc, FOAF["primaryTopic"], message))
        
        try:
                 
            store.add((message, SIOC['id'], Literal(self.getSwamlId())))
            store.add((message, SIOC['link'], URIRef(self.getXhtmlUrl())))  
            store.add((message, SIOC['has_container'],URIRef(self.config.get('base')+'forum')))   
            store.add((message, SIOC["has_creator"], URIRef(self.getSender().getUri())))                    
            store.add((message, DC['title'], Literal(self.getSubject()))) 
            store.add((message, DCT['created'], Literal(self.getDate(), datatype=XSD[u'dateTime'])))  
            
            parent = self.getParent()
            if (parent != None):
                store.add((message, SIOC['reply_of'], URIRef(parent)))  
                
            if (len(self.childs) > 0):
                for child in self.childs:
                    store.add((message, SIOC['has_reply'], URIRef(child)))
                
            previous = self.getPreviousByDate()
            if (previous != None):
                store.add((message, SIOC['previous_by_date'], URIRef(previous)))
                
            next = self.getNextByDate()
            if (next != None):
                store.add((message, SIOC['next_by_date'], URIRef(next)))                
            
            store.add((message, SIOC['content'], Literal(self.getBody())))
            
        except Exception, detail:
            print 'Error proccesing message ' + str(self.getId()) + ': ' + str(detail) 
        
        #and dump to disk
        try:
            rdf_file = open(self.getRdfPath(), 'w+')
            rdf_file.write(store.serialize(format="pretty-xml"))
            rdf_file.flush()
            rdf_file.close()        
        except IOError, detail:
            print 'IOError saving message ' + str(self.getId()) + ': ' + str(detail)
            
    def toXHTML(self):
        """
        Print a message into XHTML+RDFa format
        """
        
        #root nodes
        doc = getDOMImplementation().createDocument(None, 'html', None)
        doctype = DocumentType("html")
        doctype.publicId = "-//W3C//DTD XHTML+RDFa 1.0//EN"
        doctype.systemId = "http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd"
        doc.doctype = doctype
        root = doc.documentElement
        root.setAttribute('xmlns', 'http://www.w3.org/1999/xhtml')
        root.setAttribute('xmlns:sioc', str(SIOC))
        root.setAttribute('xmlns:foaf', str(FOAF))
        root.setAttribute('xmlns:dc', str(DC))
        root.setAttribute('xmlns:dct', str(DCT))
        root.setAttribute('xmlns:mvcb', str(MVCB))
        root.setAttribute('xmlns:xsd', str(XSD))
        
        head = doc.createElement('head')
        root.appendChild(head)
        head.setAttribute('profile', 'http://www.w3.org/2003/g/data-view')
        link = doc.createElement('link')
        link.setAttribute('rel', 'transformation')
        link.setAttribute('href', 'http://www-sop.inria.fr/acacia/soft/RDFa2RDFXML.xsl')
        head.appendChild(link)
        link = doc.createElement('link')
        link.setAttribute('rel', 'meta')
        link.setAttribute('type', 'application/rdf+xml')
        link.setAttribute('title', 'SIOC')
        link.setAttribute('href', self.getRdfUrl())
        head.appendChild(link)
        link = doc.createElement('link')
        link.setAttribute('rel', 'stylesheet')
        link.setAttribute('type', 'text/css')
        link.setAttribute('href', self.config.get('base')+'swaml.css')
        head.appendChild(link)
        title = doc.createElement('title')
        title.appendChild(doc.createTextNode(self.getSubject()))
        head.appendChild(title)
        
        #body
        body = doc.createElement('body')
        body.setAttribute('typeof', 'foaf:Document')
        body.setAttribute('about', self.getXhtmlUrl())
        root.appendChild(body)
        p = doc.createElement('p')
        span = doc.createElement('span')
        span.setAttribute('rel', 'foaf:primaryTopic')
        span.setAttribute('href', self.getUri())
        body.appendChild(p)
        p.appendChild(span)           

        #post div
        div = doc.createElement('div')
        body.appendChild(div)
        div.setAttribute('typeof', 'sioc:Post')
        div.setAttribute('about', self.getUri())
        
        #post fields
        try:
            
            h1 = doc.createElement('h1')
            div.appendChild(h1)
            h1.setAttribute('property', 'dc:title')
            h1.appendChild(doc.createTextNode(self.getSubject()))
            
            p = doc.createElement('p')
            div.appendChild(p)
            strong = doc.createElement('strong')
            p.appendChild(strong)
            strong.appendChild(doc.createTextNode('From: '))
            a = doc.createElement('a')
            a.setAttribute('rel', 'sioc:has_creator')
            a.setAttribute('href', self.getSender().getUri())
            a.appendChild(doc.createTextNode(self.getSender().getName()))
            p.appendChild(a)
            
            p = doc.createElement('p')
            div.appendChild(p)
            strong = doc.createElement('strong')
            p.appendChild(strong)
            strong.appendChild(doc.createTextNode('To: '))
            a = doc.createElement('a')
            a.setAttribute('rel', 'sioc:has_container')
            a.setAttribute('href', self.config.get('base')+'forum')
            if (len(self.config.get('title'))>0):
                a.appendChild(doc.createTextNode(self.config.get('title')))
            else:
                a.appendChild(doc.createTextNode(self.config.get('base')+'forum'))
            p.appendChild(a)
            
            p = doc.createElement('p')
            div.appendChild(p)
            strong = doc.createElement('strong')
            p.appendChild(strong)
            strong.appendChild(doc.createTextNode('Date: '))
            span = doc.createElement('span')
            span.setAttribute('property', 'dct:created')
            span.setAttribute('datatype', 'xsd:dateTime')
            span.appendChild(doc.createTextNode(self.getDate()))
            p.appendChild(span)
            
            #p = doc.createElement('p')
            #div.appendChild(p)
            #strong = doc.createElement('strong')
            #p.appendChild(strong)
            #strong.appendChild(doc.createTextNode('Message-Id: '))
            #span = doc.createElement('span')
            #span.setAttribute('property', 'sioc:id')
            #span.appendChild(doc.createTextNode(self.getSwamlId()))
            #p.appendChild(span)
            
            pre = doc.createElement('pre')
            div.appendChild(pre)
            pre.setAttribute('property', 'sioc:content')
            pre.appendChild(doc.createTextNode(self.getBody())) #FIXME: parse URLs


            p = doc.createElement('p')
            div.appendChild(p)
            p.appendChild(doc.createTextNode('URI: '))
            a = doc.createElement('a')
            a.setAttribute('href', self.getUri())
            a.appendChild(doc.createTextNode(self.getUri()))
            p.appendChild(a) 

            p = doc.createElement('p')
            div.appendChild(p)
            p.appendChild(doc.createTextNode('Link: '))
            a = doc.createElement('a')
            a.setAttribute('rel', 'sioc:link')
            a.setAttribute('href', self.getXhtmlUrl())
            a.appendChild(doc.createTextNode(self.getXhtmlUrl()))
            p.appendChild(a) 
            
            parent = self.getParent()
            if (parent != None):
                p = doc.createElement('p')
                div.appendChild(p)
                p.appendChild(doc.createTextNode('Reply of: '))
                a = doc.createElement('a')
                a.setAttribute('rel', 'sioc:reply_of')
                a.setAttribute('href', parent)
                a.appendChild(doc.createTextNode(parent))
                p.appendChild(a)
                
            if (len(self.childs) > 0):
                for child in self.childs:
                    p = doc.createElement('p')
                    div.appendChild(p)
                    p.appendChild(doc.createTextNode('Has reply: '))
                    a = doc.createElement('a')
                    a.setAttribute('rel', 'sioc:has_reply')
                    a.setAttribute('href', child)
                    a.appendChild(doc.createTextNode(child))
                    p.appendChild(a)
                
            previous = self.getPreviousByDate()
            if (previous != None):
                p = doc.createElement('p')
                div.appendChild(p)
                p.appendChild(doc.createTextNode('Previous by Date: '))
                a = doc.createElement('a')
                a.setAttribute('rel', 'sioc:previous_by_date')
                a.setAttribute('href', previous)
                a.appendChild(doc.createTextNode(previous))
                p.appendChild(a)                
                
            next = self.getNextByDate()
            if (next != None):
                p = doc.createElement('p')
                div.appendChild(p)
                p.appendChild(doc.createTextNode('Next by Date: '))
                a = doc.createElement('a')
                a.setAttribute('rel', 'sioc:next_by_date')
                a.setAttribute('href', next)
                a.appendChild(doc.createTextNode(next))
                p.appendChild(a)
            
        except Exception, detail:
            print 'Error exporting to XHTML message ' + str(self.getId()) + ': ' + str(detail) 
       
        #credits
        p = doc.createElement('p')
        body.appendChild(p)
        p.setAttribute('class', 'credits')
        a = doc.createElement('a')
        a.setAttribute('rel', 'mvcb:generatorAgent')
        a.setAttribute('href', 'http://swaml.berlios.de/')
        a.appendChild(doc.createTextNode('Generated by '))
        abbr = doc.createElement('abbr')
        abbr.setAttribute('title', 'Semantic Web Archives of Mailing Lists')
        abbr.appendChild(doc.createTextNode('SWAML'))
        a.appendChild(abbr)
        p.appendChild(a)
        
        
        #and dump to disk
        try:
            xhtml_file = open(self.getXhtmlPath(), 'w+') #FIXME
            try:
                xml.dom.minidom.Document.toprettyxml(doc, xhtml_file)
            except UnicodeDecodeError, detail:
                xhtml_file.write("")
                print 'Decode error saving message ' + str(self.getId()) + ': ' + str(detail)
            xhtml_file.flush()
            xhtml_file.close()
        except IOError, detail:
            print 'IOError saving message ' + str(self.getId()) + ': ' + str(detail)            
            
    def __calculateId(self):
        """
        Calculate SWAML ID

        @todo: obtain a better SWAML ID
        """
        
        #id: hashcode of 'MessageId - Date + ID'
        self.swamlId = sha.new(self.messageId + '-' + self.date + '-swaml-' + str(self.id)).hexdigest()            

