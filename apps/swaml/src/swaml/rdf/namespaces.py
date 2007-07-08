# -*- coding: utf8 -*-

# SWAML KML Exporter <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2005-2007 Sergio Fernández
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

SIOC = Namespace(u'http://rdfs.org/sioc/ns#')
RDF = Namespace(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = Namespace(u'http://www.w3.org/2000/01/rdf-schema#')
DC = Namespace(u'http://purl.org/dc/elements/1.1/')
DCTERMS = Namespace(u'http://purl.org/dc/terms/')
FOAF = Namespace(u'http://xmlns.com/foaf/0.1/')
GEO = Namespace(u'http://www.w3.org/2003/01/geo/wgs84_pos#')
MVCB = Namespace(u'http://webns.net/mvcb/')
ICAL = Namespace(u'http://www.w3.org/2002/12/cal/icaltzd#')
