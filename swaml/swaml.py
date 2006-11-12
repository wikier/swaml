#!/usr/bin/env python2.4
# -*- coding: utf8 -*-
#
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

"""Semantic Web Archive of Mailing Lists"""

import sys, string
from classes.ui import CommandLineUI
from classes.configuration import Configuration
from classes.mailinglist import MailingList

class SWAML(CommandLineUI):
    """
    Main class of SWAML project
    
    @author: Sergio Fdez
    @license: GPL
    """

    def parseArgs(self, argv):
        """
        Getting params of default input
        
        @param argv: arguments values array
        """
        
        if not self.config.parse(argv):
            self.usage()
            
        #self.config.show()

    def __init__(self, argv):
        """
        main method
        @param argv: values of inline arguments
        """
        
        CommandLineUI.__init__(self, 'swaml')
        
        self.config = Configuration()        
        
        for arg in argv:
            if arg == "-h" or arg == "--help":
                self.usage()
            elif arg == "-v" or arg == "--verbose":
                self.config.set('verbose', True)
                
        self.config.setAgent('http://swaml.berlios.de/doap.rdf')
        self.parseArgs(argv)
        self.list = MailingList(self.config)
        messages = self.list.publish()
        print str(messages), 'messages procesed'



if __name__ == '__main__':
    try:
        SWAML(sys.argv[1:])
    except KeyboardInterrupt:
        print 'Received Ctrl+C or another break signal. Exiting...'

                                                                            
del sys, string

