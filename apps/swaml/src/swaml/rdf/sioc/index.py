# -*- coding: utf8 -*-

# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2005-2006 Sergio Fernández
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

"""Indexing messages"""

import sys, os, string, sha

class Index:
    """
    Messages index
    """
    
    def __init__(self, config):
        """
        Index constructor
        
        @param config: reference to the configuration
        """
        
        self.config = config
        self.items = []
        self.translateIndex = {}
        
    def add(self, new):
        """
        Add new item
        
        @param new: new item
        """
        
        #store message
        self.items.append(new)
        
        #and translation
        id = new.getMessageId() #FIXME, bug #8295   
        if (id in self.translateIndex):
            print 'Duplicated message id: ' + id + ' (see more on bug #8295)'
        #deliberately only we maintain the reference with the most 
        # recent message with this id (bug #8295)
        self.translateIndex[id] = len(self.items)
            
    def get(self, id):
        """
        Get message who has an ID
        
        @param id: message id
        @return: message
        """
        
        return self.getMessage(self.__getTranslation(id))
        
    def getMessage(self, n):
        """
        Get a message
        
        @param n: message numeric id
        """
        if (n != None and n <= len(self.items)):
            return self.items[n-1]
        else:
            return None

    def getMessageByUri(self, uri):
        """
        Get a message by URI
        
        @param uri: message uri
        """
        for msg in self.items:
            if (uri == msg.getUri()):
                return msg
        return None
        
    def __getTranslation(self, id):
        """
        Get the reference translation
        
        @param id: message id
        @return: translation
        """
        
        if (id in self.translateIndex):
            return self.translateIndex[id]
        else:
            return None
                
    def getMessagesUri(self):
        """
        Get all URIs into a list
        
        @return: messages uris
        """
        uris = []
        
        for msg in self.items:
            uris.append(msg.getUri())
            
        return uris
    
        
