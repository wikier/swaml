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
import lxml.html

class Resource:
    """
    Abstract RDF Resource
    """

    def __init__(self, base):
        self.base = base
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
        return self.get_graph().serialize(format="pretty-xml", encoding="utf8") #, base=self.base)

    def get_data_n3(self):
        return self.get_graph().serialize(format="n3", encoding="utf8") #, base=self.base)

class Post(Resource):
    """
    sioc:Post
    """

    def __init__(self, base, id, title, content):
        self.base = base
        self.id = id
        self.title = title
        self.content = lxml.html.fromstring(content).text_content()
        #FIXME: actually more stuff would be necessary, but this is the minimun

    def get_uri(self):
        return "%s#message" % self.base #FIXME

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
        graph.bind('mvcb', MVCB)

        swaml = URIRef("http://swaml.berlios.de/doap#swaml")
        doc = URIRef(self.base)
        graph.add((doc, RDF.type, FOAF["Document"]))
        graph.add((doc, RDFS.label, Literal("RDF version of the message '%s' retrieved from MarkMail API" % self.id))) #FIXME: this should go out of this api
        graph.add((doc, MVCB.generatorAgent, swaml))
        message = URIRef(self.get_uri())
        graph.add((message, RDF.type, SIOC.Post))
        graph.add((doc, FOAF.primaryTopic, message))

        graph.add((message, SIOC.id, Literal(self.id)))
        graph.add((message, SIOC.link, URIRef("http://markmail.org/message/%s" % self.id)))  
        #graph.add((message, SIOC.has_container,URIRef(self.config.get('base')+'forum')))   
        #graph.add((message, SIOC.has_creator, URIRef(self.getSender().getUri())))                    
        graph.add((message, DCT.title, Literal(self.title))) 
        #graph.add((message, DCT.created, Literal(self.getDate(), datatype=XSD[u'dateTime'])))  
        graph.add((message, SIOC.content, Literal(self.content)))

        self.set_graph(graph)

class Thread(Resource):

    def __init__(self, base, id, title, homepage, atom, messages=[]):
        self.base = base
        self.id = id
        self.title = title
        self.homepage = homepage
        self.atom = atom
        self.messages = messages

    def get_uri(self):
        return "%s#thread" % self.base #FIXME

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
        graph.bind('mvcb', MVCB)

        swaml = URIRef("http://swaml.berlios.de/doap#swaml")
        doc = URIRef("%s/thread/%s" % (self.base, self.id))
        graph.add((doc, RDF.type, FOAF["Document"]))
        graph.add((doc, RDFS.label, Literal("RDF version of the thread '%s' retrieved from MarkMail API" % self.id))) #FIXME: this should go out of this api
        graph.add((doc, MVCB.generatorAgent, swaml))
        thread = URIRef("%s/thread/%s#thread" % (self.base, self.id))
        graph.add((thread, RDF.type, SIOC["Thread"]))
        graph.add((doc, FOAF["primaryTopic"], thread))

        graph.add((thread, SIOC.id, Literal(self.id)))
        graph.add((thread, SIOC.link, URIRef(self.homepage)))              
        graph.add((thread, DCT.title, Literal(self.title))) 
        graph.add((thread, SIOC.num_item, Literal(len(self.messages), XSD.Integer))) 
        for message in self.messages:
            url = "%s/message/%s" % (self.base, message["id"])
            post = URIRef("%s#message" % url)
            graph.add((post, RDF.type, SIOC.Post))
            graph.add((post, RDFS.seeAlso, URIRef(url)))
            graph.add((thread, SIOC.container_of, post))
            graph.add((post, SIOC.has_container, thread))
            graph.add((post, SIOC.id, Literal(self.id)))
            graph.add((post, SIOC.link, URIRef("http://markmail.org%s" % message["url"])))  
            author = BNode()
            graph.add((post, SIOC.has_creator, author))
            graph.add((author, RDF.type, SIOC.UserAccount))
            graph.add((author, SIOC.name, Literal(message["from"])))
            graph.add((post, DCT.created, Literal(message["date"], datatype=XSD.dateTime)))

        self.set_graph(graph)


