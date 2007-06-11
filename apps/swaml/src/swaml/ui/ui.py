# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2005-2007 Sergio Fdez
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

"""Common functions for UIs"""

import sys, os, string

class UI:
    """
    Abstract class for User Interfaces
    """
    
    def usage(self):
        """
        Print usage information
        """
        
        pass
    
    def __init__(self, id=None, base='./'):
        """
        Constructor method
        
        @param id: string id
        @param base: base directory
        """
        
        self.id = id
        self.base = base
