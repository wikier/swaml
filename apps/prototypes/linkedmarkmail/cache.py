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
import warnings
import logging
from utils import serialize_graph_file, read_graph, exists

class Cache:
    """
    A very simple implementation of a RDF cache system on disk
    """

    def __init__(self, base="cache/"):
        self.base = base
        self.__registry = {}
        self.__last_read = {}

    def register(self, cls, tpl):
        self.__registry[cls] = tpl

    def __build_path(self, key, cls):
        tpl = self.__registry[cls]
        return self.base + tpl % key

    def has_key(self, key, cls):
        if (cls in self.__registry):
            path = self.__build_path(key, cls)
            return exists(path)
        else:
            return False

    def is_cached(self, item):
        path = self.__build_path(item.get_key(), item.__class__)
        return exists(path)

    def is_dirty(self, item):
        graph = item.get_graph()
        cached = self.read(item.get_key(), item.__class__)
        if (len(graph) > len(cached)):
            return True
        else:
            return False

    def read(self, key, cls):
        if (cls in self.__registry):
            id = self.__registry[cls] % key
            if (id in self.__last_read):
                logging.debug("Preventing reading of %s" % id)
                return self.__last_read[id]
            else:
                path = self.__build_path(key, cls)
                data = read_graph(path)
                self.__last_read = {} #FIXME: current it has only one item, which can be the right length?
                self.__last_read[id] = data
                return data
        else:
            return ""

    def write(self, item):
        path = self.__build_path(item.get_key(), item.__class__)
        graph = item.get_graph()
        serialize_graph_file(graph, path)

    def update(self, item, force=True):
        if (force):
            self.write(item)
            return True
        else:
            if (self.is_dirty(item)):
                self.write(item)
                return True
            else:
                return False

