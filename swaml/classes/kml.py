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

"""Google KML basic support"""

import sys, os, string

class KML:
    """
    KML format support
    """
    
    def __init__(self):
        """
        KML document constructor
        """
        self.places = []
        self.ns = 'http://earth.google.com/kml/2.0'
        
    def addPlace(self, lat, lon, name=None, description=None):
        """
        Add a new placemark
        """
        self.places.append(Place(lat, lon, name, description))
        
    def write(self, file):
        """
        Serialize into KML 2.0 format
        """
        import xml.dom.minidom
        from   xml.dom.minidom import getDOMImplementation
        from   xml.dom.ext     import PrettyPrint
        
        #root nodes
        doc  = getDOMImplementation().createDocument(None, "kml", None)
        root = doc.documentElement
        root.setAttribute('xmlns', self.ns)
        
        #and placesmarks
        for place in self.places:
            placemark = doc.createElement('Placemark')
            root.appendChild(placemark)
            
            #information nodes
            name_text = place.getName()
            if (name_text != None):
                name = doc.createElement('name')
                name.appendChild(doc.createTextNode(name_text))
                placemark.appendChild(name)
            
            pic = place.getDescription()
            if (pic != None):
                description = doc.createElement('description')
                desc = '<img src="'+pic+'" />'
                description.appendChild(doc.createTextNode(desc))
                placemark.appendChild(description)
            
            #look at node
            lookAt = doc.createElement('LookAt')
            placemark.appendChild(lookAt)
            
            #coordinates
            latitude, longitude = place.getCoordinates()
            lat = doc.createElement('latitude')
            lat.appendChild(doc.createTextNode(str(latitude)))
            lookAt.appendChild(lat)
            lon = doc.createElement('longitude')
            lon.appendChild(doc.createTextNode(str(longitude)))
            lookAt.appendChild(lon)   
            
            #other vars
            #range = doc.createElement('range')
            #range.appendChild(doc.createTextNode('0'))
            #lookAt.appendChild(range)
            #tilt = doc.createElement('tilt')
            #tilt.appendChild(doc.createTextNode('0'))
            #lookAt.appendChild(tilt)
            #heading = doc.createElement('heading')
            #heading.appendChild(doc.createTextNode('0'))
            #lookAt.appendChild(heading)
            #TODO: read KML specification to learn what are            
            
            #point
            point = doc.createElement('Point')
            coordinates = doc.createElement('coordinates')
            coordinates.appendChild(doc.createTextNode(str(longitude) + ',' + str(latitude) + ',0'))
            point.appendChild(coordinates)
            placemark.appendChild(point)
                                 
        
        #and dump it in pretty xml format
        xml.dom.ext.PrettyPrint(doc, file)
        
    

class Place:
    
        def __init__(self, lat, lon, name=None, description=None):
            """
            New placemark
            """
            self.name = name
            self.description = description
            self.lat = lat
            self.lon = lon
            
        def getName(self):
            """
            Get placemark name
            """
            return self.name
        
        def getDescription(self):
            """
            Get placemark description
            """
            return self.description
        
        def getCoordinates(self):
            """
            Get placemark coordinates
            """
            return [self.lat, self.lon]