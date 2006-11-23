#!/usr/bin/env python2.4
# -*- coding: utf8 -*-
#
# SWAML KML Exporter <http://swaml.berlios.de/>
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

"""Wizard to create config files for SWAML"""

import sys, os, string
from classes.ui import CommandLineUI
from classes.configuration import Configuration
import ConfigParser

class ConfigWizard(CommandLineUI):
    """
    SWAML's config wizard
    
    @author: Sergio Fdez
    @license: GPL
    """
    
    def requestData(self):
        self.config = Configuration()
        
        print 'Write your configuration options:'
        print '(default value goes between [...])'
        
        for var in self.config.config.keys():
            defaultValue = str(self.config.config[var])
            value = raw_input('\t - ' + var + '[' + defaultValue + ']: ')
            if (len(value) > 0):
                self.config.set(var, value)
    
    def printData(self):
        
        ini = ConfigParser.ConfigParser()
        
        ini.add_section(self.section)
        
        for var in self.config.config.keys():
            ini.set(self.section, var, str(self.config.config[var]))
                     
        try:
            file = open(self.output, 'w+')
            ini.write(file)
            file.flush()
            file.close()
            print 'new config file created in', self.output, 'with chosen parameters'
        except IOError, detail:
            print 'Error exporting coordinates config file: ' + str(detail)
    
    def wizard(self):
        self.requestData()
        self.printData()
        
    def __init__(self, argv):
        """
        main method
        @param argv: values of inline arguments
        """       
        
        CommandLineUI.__init__(self, 'configWizard')
        
        self.section = 'SWAML'
        
        for arg in argv:
            if arg == "-h" or arg == "--help":
                self.usage()
                
        if (len(argv)>=1):
            self.output = argv[0]
            self.wizard()
        else:
            self.usage()


if __name__ == '__main__':
    try:
        ConfigWizard(sys.argv[1:])
    except KeyboardInterrupt:
        print 'Received Ctrl+C or another break signal. Exiting...'

                                                                            
del sys, os, string
