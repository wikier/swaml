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

"""Code to work over a mailbox file"""

import os, sys,string, mailbox

class Mbox:
    """mbox abstraction class"""

    def __init__(self, path):
        """Constructor method"""

        self.path = path

        try:
            self.mbox_file = mailbox.UnixMailbox(open(self.path))
        except IOError:
            print "mbox file does not exist, exiting gracefully"
            sys.exit()
    

    def nextMessage(self):
        """Return next message of mbox file"""
        
        return self.mbox_file.next()
        


    

