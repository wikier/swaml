# -*- coding: utf8 -*-

# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2005-2007 Sergio Fernández
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
from swaml.rdf.namespaces import SIOC, RDFS, FOAF, DC, DCTERMS
from swaml.common.charset import Charset
from swaml.common.date import MailDate, FileDate
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
from xml.dom.ext import PrettyPrint

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
        
        #body after indexing all messages
        self.body = None
        #self.body = msg.fp.read()
        #[(self.body, enconding)] = decode_header(msg.fp.read())
        
        self.obtainPath()
        
    def setBody(self, body):
        """
        Set body content
        
        @param body: content
        """
        
        self.body = body
        
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
        
    def getPath(self):
        """
        Return the message's index name
        
        @return: path
        """
        
        return self.path
    
    def obtainPath(self):
        """
        Obtain message path
        """

        #replace vars        
        #FIXME: format permited vars (feature #1355)
        index = self.config.get('format')
        
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
    
    def getUri(self):    
        """
        Get message URI
        
        @return: uri
        """
                
        return self.config.get('url') + 'post/' + self.dir + str(self.id)
    
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
        store.bind('dcterms', DCTERMS)
        
        #message node
        message = URIRef(self.getUri())
        store.add((message, RDF.type, SIOC["Post"]))
        
        try:
                 
            store.add((message, SIOC['id'], Literal(self.getSwamlId())))
            store.add((message, SIOC['link'], URIRef(self.getUri())))  
            store.add((message, SIOC['has_container'],URIRef(self.config.get('url')+'forum')))   
            store.add((message, SIOC["has_creator"], URIRef(self.getSender().getUri())))                    
            store.add((message, DC['title'], Literal(self.getSubject()))) 
            store.add((message, DCTERMS['created'], Literal(self.getDate())))  
            
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
            rdf_file = open(self.config.get('dir') + self.getPath(), 'w+')
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
        doc = getDOMImplementation().createDocument(None, "html", None)
        root = doc.documentElement
        root.setAttribute('xmlns', 'http://www.w3.org/1999/xhtml')
        root.setAttribute('xmlns:sioc', str(SIOC))
        root.setAttribute('xmlns:dc', str(DC))
        root.setAttribute('xmlns:dcterms', str(DCTERMS))
        head = doc.createElement('head')
        root.appendChild(head)
        title = doc.createElement('title')
        title.appendChild(doc.createTextNode(self.getSubject()))
        head.appendChild(title)
        body = doc.createElement('body')
        root.appendChild(body)
        
        #post div
        div = doc.createElement('div')
        body.appendChild(div)
        div.setAttribute('class', 'sioc:Post')
        div.setAttribute('about', self.getUri())
        
        try:
            
            p = doc.createElement('p')
            div.appendChild(p)
            p.appendChild(doc.createTextNode('Subject: '))
            span = doc.createElement('span')
            span.setAttribute('class', 'dc:title')
            span.appendChild(doc.createTextNode(self.getSubject()))
            p.appendChild(span)            
            
            p = doc.createElement('p')
            div.appendChild(p)
            p.appendChild(doc.createTextNode('Message-Id: '))
            span = doc.createElement('span')
            span.setAttribute('class', 'sioc:id')
            span.appendChild(doc.createTextNode(self.getSwamlId()))
            p.appendChild(span)
            
            p = doc.createElement('p')
            div.appendChild(p)
            p.appendChild(doc.createTextNode('Forum: '))
            span = doc.createElement('span')
            span.setAttribute('class', 'sioc:has_container')
            span.appendChild(doc.createTextNode(self.config.get('url')+'forum'))
            p.appendChild(span)
            
            p = doc.createElement('p')
            div.appendChild(p)
            p.appendChild(doc.createTextNode('Author: '))
            a = doc.createElement('a')
            a.setAttribute('class', 'sioc:has_creator')
            a.setAttribute('href', self.getSender().getUri())
            a.appendChild(doc.createTextNode(self.getSender().getUri()))
            p.appendChild(a)
                                        
            p = doc.createElement('p')
            div.appendChild(p)
            p.appendChild(doc.createTextNode('Date: '))
            span = doc.createElement('span')
            span.setAttribute('class', 'dcterms:created')
            span.appendChild(doc.createTextNode(self.getDate()))
            p.appendChild(span)
            
            parent = self.getParent()
            if (parent != None):
                p = doc.createElement('p')
                div.appendChild(p)
                p.appendChild(doc.createTextNode('Reply of: '))
                a = doc.createElement('a')
                a.setAttribute('class', 'sioc:reply_of')
                a.setAttribute('href', parent)
                a.appendChild(doc.createTextNode(parent))
                p.appendChild(a)
                
            if (len(self.childs) > 0):
                for child in self.childs:
                    p = doc.createElement('p')
                    div.appendChild(p)
                    p.appendChild(doc.createTextNode('Has reply: '))
                    a = doc.createElement('a')
                    a.setAttribute('class', 'sioc:has_reply')
                    a.setAttribute('href', child)
                    a.appendChild(doc.createTextNode(child))
                    p.appendChild(a)
                
            previous = self.getPreviousByDate()
            if (previous != None):
                p = doc.createElement('p')
                div.appendChild(p)
                p.appendChild(doc.createTextNode('Previous by Date: '))
                a = doc.createElement('a')
                a.setAttribute('class', 'sioc:previous_by_date')
                a.setAttribute('href', previous)
                a.appendChild(doc.createTextNode(previous))
                p.appendChild(a)                
                
            next = self.getNextByDate()
            if (next != None):
                p = doc.createElement('p')
                div.appendChild(p)
                p.appendChild(doc.createTextNode('Next by Date: '))
                a = doc.createElement('a')
                a.setAttribute('class', 'sioc:next_by_date')
                a.setAttribute('href', next)
                a.appendChild(doc.createTextNode(next))
                p.appendChild(a)
            
            pre = doc.createElement('pre')
            div.appendChild(pre)
            pre.setAttribute('class', 'sioc:content')
            pre.appendChild(doc.createTextNode(self.getBody())) 
            
        except Exception, detail:
            print 'Error exporting to XHTML message ' + str(self.getId()) + ': ' + str(detail) 
        
        #and dump to disk
        try:
            xhtml_file = open(self.config.get('dir') +  '.'.join(self.getPath().split('.')[:-1]) + '.xhtml', 'w+') #FIXME
            xml.dom.ext.PrettyPrint(doc, xhtml_file)
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
        

        


        
