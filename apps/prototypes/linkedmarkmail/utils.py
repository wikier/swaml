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

import os
from StringIO import StringIO
try:
    from rdflib.graph import ConjunctiveGraph
except ImportError:
    from rdflib import ConjunctiveGraph

def exists(path):
    return os.path.exists(path)

def read_file(path):
    data = ""
    f = open(path, "r")
    while 1:
        line = f.readline()
        if not line:
            break
        data += line
    f.close()
    return data

def read_graph(path, base=None, format="xml"):
    data = read_file(path)
    graph = ConjunctiveGraph()
    graph.parse(StringIO(data), publicID=base, format=format)
    return graph

def serialize_graph_file(graph, path, format="pretty-xml", encoding="utf8"):
    f = open(path, "w")
    graph.serialize(destination=f, format=format, encoding=encoding)
    f.flush()
    f.close()

def write_file(data, path, mode="w"):
    f = open(path, mode)
    f.write(data)
    f.flush()
    f.close()

