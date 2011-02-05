# -*- coding: utf8 -*-

# SWAML new API (alpha)
#
# Copyright (C) 2011 Sergio Fernández
#
# This file is part of SWAML <http://swaml.berlios.de/>
# 
# SWAML is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# SWAML is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with SWAML. If not, see <http://www.gnu.org/licenses/>.


"""
The new SWAML API (alpha)
"""

import warnings
try:
    from rdflib.graph import ConjunctiveGraph
except ImportError:
    from rdflib import ConjunctiveGraph
from rdflib import URIRef, Literal, BNode
from rdflib import RDF
from namespaces import SIOC, RDFS, FOAF, DC, DCT, MVCB, XSD

class Resource:
    """
    Abstract RDF Resource
    """

    def __init__(self):
        raise NotImplementedError

    def get_uri(self):
        return self.uri

    def set_uri(self, uri):
        self.uri = uri

    def get_graph(self):
        if (not hasattr(self, "graph") or self.graph == None):
            self.__build_graph()
        return self.graph

    def set_graph(self, graph):
        self.graph = graph

    def __build_graph(self):
        warnings.warn("This method MUST be overwritten by all subclasses!")
        return ConjunctiveGraph()

    def get_data_xml(self):
        return self.get_graph().serialize(format="pretty-xml")

    def get_data_n3(self):
        return self.get_graph().serialize(format="n3")

class Post(Resource):
    """
    sioc:Post
    """

    def __init__(self, title, content, id=None, url=None):
        self.title = title
        self.content = content
        self.id = id
        self.url = url
        #FIXME: actually more stuff would be necessary, but this is the minimun

    def get_uri(self):
        return "%s#post" % self.url #FIXME

    def get_graph(self):
        if (not hasattr(self, "graph") or self.graph == None):
            self.__build_graph()
        return self.graph

    def __build_graph(self):
        graph = ConjunctiveGraph()
        graph.bind('sioc', SIOC)
        graph.bind('foaf', FOAF)
        graph.bind('rdfs', RDFS)
        graph.bind('dct', DCT)

        doc = URIRef(self.url)
        graph.add((doc, RDF.type, FOAF["Document"]))
        message = URIRef(self.get_uri())
        graph.add((message, RDF.type, SIOC["Post"]))
        graph.add((doc, FOAF["primaryTopic"], message))

        graph.add((message, SIOC['id'], Literal(self.id)))
        #graph.add((message, SIOC['link'], URIRef(self.url)))  
        #graph.add((message, SIOC['has_container'],URIRef(self.config.get('base')+'forum')))   
        #graph.add((message, SIOC["has_creator"], URIRef(self.getSender().getUri())))                    
        graph.add((message, DCT['title'], Literal(self.title))) 
        #graph.add((message, DCT['created'], Literal(self.getDate(), datatype=XSD[u'dateTime'])))  
        graph.add((message, SIOC['content'], Literal(self.content)))

        self.set_graph(graph)

