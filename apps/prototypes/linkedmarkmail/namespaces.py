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

"""Common namespaces"""

from rdflib import Namespace

RDF   = Namespace(u"http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS  = Namespace(u"http://www.w3.org/2000/01/rdf-schema#")
SWAML = Namespace(u"http://swaml.berlios.de/ns/0.3#")
SIOC  = Namespace(u"http://rdfs.org/sioc/ns#")
SIOCT = Namespace(u"http://rdfs.org/sioc/types#")
DC    = Namespace(u"http://purl.org/dc/terms/")
DCT   = Namespace(u"http://purl.org/dc/terms/")
FOAF  = Namespace(u"http://xmlns.com/foaf/0.1/")
GEO   = Namespace(u"http://www.w3.org/2003/01/geo/wgs84_pos#")
MVCB  = Namespace(u"http://webns.net/mvcb/")
ICAL  = Namespace(u"http://www.w3.org/2002/12/cal/icaltzd#")
XSD   = Namespace(u"http://www.w3.org/2001/XMLSchema#")

NSbindings = {
    u"rdf"   : RDF,
    u"rdfs"  : RDFS,
    u"swaml" : SWAML,
    u"sioc"  : SIOC,
    u"sioct" : SIOCT,
    u"dc"    : DC,
    u"dct"   : DCT,
    u"foaf"  : FOAF,
    u"geo"   : GEO,
    u"mvcb"  : MVCB,
    u"ical"  : ICAL,
    u"xsd"   : XSD
}

