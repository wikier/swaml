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

"""Util function to work with charsets"""

import sys, os, string
from email.Header import decode_header


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
        
