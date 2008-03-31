# -*- coding: utf8 -*-

# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2005-2008 Sergio Fernández, Diego Berrueta
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

"""Common namespaces"""

from rdflib import Namespace

RDF   = Namespace(u"http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS  = Namespace(u"http://www.w3.org/2000/01/rdf-schema#")
SIOC  = Namespace(u"http://rdfs.org/sioc/ns#")
SIOCT = Namespace(u"http://rdfs.org/sioc/types#")
DC    = Namespace(u"http://purl.org/dc/elements/1.1/")
DCT   = Namespace(u"http://purl.org/dc/terms/")
FOAF  = Namespace(u"http://xmlns.com/foaf/0.1/")
GEO   = Namespace(u"http://www.w3.org/2003/01/geo/wgs84_pos#")
MVCB  = Namespace(u"http://webns.net/mvcb/")
ICAL  = Namespace(u"http://www.w3.org/2002/12/cal/icaltzd#")
XSD   = Namespace(u"http://www.w3.org/2001/XMLSchema#")

bindings = {
                u"http://www.w3.org/1999/02/22-rdf-syntax-ns#" : rdf,
                u"http://www.w3.org/2000/01/rdf-schema#" : rdfs,
                u"http://rdfs.org/sioc/ns#" : sioc,
                u"http://rdfs.org/sioc/types#" : sioct,
                u"http://purl.org/dc/elements/1.1/" : dc,
                u"http://purl.org/dc/terms/" : dct,
                u"http://xmlns.com/foaf/0.1/" : foaf,
                u"http://www.w3.org/2003/01/geo/wgs84_pos#" : geo,
                u"http://webns.net/mvcb/" : mvcb,
                u"http://www.w3.org/2002/12/cal/icaltzd#" : ical,
                u"http://www.w3.org/2001/XMLSchema#" : xsd
          }

