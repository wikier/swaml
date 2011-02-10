# -*- coding: utf8 -*-

# LinkedMarkMail, an RDFizer for Mark Mail 
#
# Copyright (C) 2011 Sergio Fernández
#
# This file is part of SWAML <http://swaml.berlios.de/>
# 
# LinkedMarkMail is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# LinkedMarkMail is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with LinkedMarkMail. If not, see <http://www.gnu.org/licenses/>.

import sys
from utils import serialize_graph_file, read_graph

class Cache:
    """
    A very simple implementation of a RDF cache system on disk
    """

    def __init__(self, base="cache/"):
        self.base = base

    def write(self, item):
        path = self.base + item.get_cache_id()
        graph = item.get_graph()
        serialize_graph_file(graph, path)

    def update(self, item):
        path = self.base + item.get_cache_id()
        graph = item.get_graph()
        cached = read_graph(path)
        if (len(graph) > len(cached):
            self.write(item)

class CacheItem:
    """
    Cache item pseudo interface
    """

    def get_cache_id(self):
        warnings.warn("This method MUST be overwritten by cacheable items!")
        sys.exit()

    def get_graph(self):
        warnings.warn("This method MUST be overwritten by cacheable items!")
        sys.exit()

