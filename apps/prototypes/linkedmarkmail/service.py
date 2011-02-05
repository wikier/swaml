#!/usr/bin/python
# -*- coding: utf-8 -

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
import os
import logging
import cgi
import cgitb; cgitb.enable()
from linkedmarkmail import LinkedMarkMail

types = ["post", "thread"]

if __name__ == "__main__":

    form = cgi.FieldStorage()

    i = None
    t = None
    try:
        i = form["id"].value
        t = form["type"].value
    except Exception, e:
        print "Content-type: text/html; charset=utf-8"
        print "Status: 400 Invalid Input"
        print
        print "<html>"
        print "<head>"
        print "<title>Error calling the service</title>"
        print "</head>"
        print "<body>"
        print "<h1>Error calling the service</h1>"
        print e
        print "</body>"
        print "</html>"
        sys.exit(1)

    lmm = LinkedMarkMail()
    data = None
    if (t == "post"):
        data = lmm.get_message(i)
    else:
        lmm.get_thread(i)

    if (data == None):
        print "Content-type: text/html; charset=utf-8"
        print "Status: 404 Not Found"
        print
        print "<html>"
        print "<head>"
        print "<title>Error calling the service</title>"
        print "</head>"
        print "<body>"
        print "<h1>Error calling the service</h1>"
        print "The %s '%s' has not found on MarkMail" % (t, i)
        print "</body>"
        print "</html>"
        sys.exit(1)

    print "Content-type: application/rdf+xml; charset=utf-8"
    print "Cache-Control: max-age=600"
    print "Status: 200 OK"
    print
    print data
    print

