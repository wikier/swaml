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

types = ["message", "thread"]

def invalid_input_error():
    print "Content-type: text/html; charset=utf-8"
    print "Status: 400 Invalid Input"
    print
    print "<html>"
    print "<head>"
    print "<title>Error calling the service: 400 Invalid Input</title>"
    print "</head>"
    print "<body>"
    print "<h1>Error calling the service: 400 Invalid Input</h1>"
    print "Parameter '%s' required!" % e
    print "</body>"
    print "</html>"
    sys.exit(1)

def not_found_error(t, i):
    print "Content-type: text/html; charset=utf-8"
    print "Status: 404 Not Found"
    print
    print "<html>"
    print "<head>"
    print "<title>Error calling the service: 404 Not Found</title>"
    print "</head>"
    print "<body>"
    print "<h1>Error calling the service: 404 Not Found</h1>"
    print "The %s '%s' has not found on MarkMail" % (t, i)
    print "</body>"
    print "</html>"
    sys.exit(1)

def generate_response(data):
    print "Content-type: application/rdf+xml; charset=utf-8"
    print "Cache-Control: max-age=600"
    print "Status: 200 OK"
    print
    print data
    print

if __name__ == "__main__":

    form = cgi.FieldStorage()

    i = None
    t = None
    try:
        i = form["id"].value
        t = form["type"].value
    except Exception, e:
        invalid_input_error()

    lmm = LinkedMarkMail()
    data = None
    if (t == "message"):
        data = lmm.get_message(i)
    elif (t == "thread"):
        data = lmm.get_thread(i)
    else:
        invalid_input_error()

    if (data == None):
        not_found_error(t, i)

    generate_response(data)

