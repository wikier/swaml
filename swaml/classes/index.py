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

class Index:
    
    def __init__(self, config):
        self.config = config
        self.items = {}
        self.translateIndex = {}
        
    def add(self, new):
        id = new.getMessageId() #FIXME, bug #8295
        swamlId = new.getSwamlId()
        
        #store mesage
        if (swamlId in self.items):
            print 'Error adding new index item: ' + swamlId + ' is duplicated'
        else:
            self.items[swamlId] = new
            
        #and translation
        if (id in self.translateIndex):
            print 'Duplicated message id: ' + id + ' (see more on bug #8295)'
        #deliberately only we maintain the reference with the most 
        # recent message with this id (bug #8295)
        self.translateIndex[id] = swamlId
            
    def get(self, id):
        """
        Get message who has this ID
        """
        swamlId = self.__getTranslation(id)
        return self.getMessage(swamlId)
        
    def getMessage(self, id):
        """
        Get message who has this SWAML ID
        """
        if (id in self.items):
            return self.items[id]
        else:
            return None
        
    def __getTranslation(self, id):
        if (id in self.translateIndex):
            return self.translateIndex[id]
        else:
            return None
                
    def getMessagesUri(self):
        uris = []
        
        for id, msg in self.items.items():
            uris.append(msg.getUri())
            
        return uris
    
        
