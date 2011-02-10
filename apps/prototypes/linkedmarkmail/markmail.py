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


"""
A simple python client for MarkMail hacky API

Futher details at: http://pastebin.com/M5NnyEZ8
"""

import urllib
import urllib2
import simplejson as json
from StringIO import StringIO
import warnings
import logging

class MarkMail:

    def __init__(self, base="http://markmail.org", log="linkedmarkmail.log"):
        self.base = base
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s", stream=open(log, "w+")
        logging.info("Starting LinkedMarkMail" % directory)


    def search(self, query, page=1, mode="json"):
        logging.info("Searching: q=%s, page=%d, mode=%s" % (query, page, mode))
        uri = "%s/results.xqy?q=%s&page=%d&mode=%s" % (base, query, page, mode)
        response = self.__request(uri).read()
        obj = json.load(StringIO(response))
        warnings.warn("This method is still fully unimplemented")
        return obj #FIXME

    def get_message(self, key, mode="json"):
        logging.info("Getting message: key=%s, mode=%s" % (key, mode))
        uri = "%s/message.xqy?id=%s&mode=%s" % (self.base, key, mode)
        response = self.__request(uri).read()
        obj = json.load(StringIO(response))
        message = obj["message"]
        if (message["subject"]==None or message["subject"]==None):
            logging.error("Thread %s not found" % key)
            return None
        else:
            logging.info("Thread %s found!" % key)
            return message

    def get_thread(self, key, mode="json"):
        logging.info("Getting thread: key=%s, mode=%s" % (key, mode))
        uri = "%s/thread.xqy?id=%s&mode=%s" % (self.base, key, mode)
        response = self.__request(uri).read()
        obj = json.load(StringIO(response))
        thread = obj["thread"]
        if (thread["subject"]==None or thread["list"]==None):
            logging.error("Thread %s not found" % key)
            return None
        else:
            logging.info("Thread %s found!" % key)
            return thread
        
    def __request(self, uri, accept="application/json"):
        """
        Generic HTTP request
       
        @param uri: uri to request
        @return: response
        @rtype: file-like object
        """
       
        headers = {
                    "User-Agent" : "swaml (http://swaml.berlios.de/; sergio@wikier.org)",
                    "Accept"     : accept
                  }
        request = urllib2.Request(uri, headers=headers)
        return urllib2.urlopen(request)

