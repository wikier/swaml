#!/usr/bin/python
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
LinkedMarkMail, an RDFizer for Mark Mail 
"""

import logging
from datetime import datetime
from markmail import MarkMail
from swaml import Post, Thread
from cache import Cache

class LinkedMarkMail:

    def __init__(self, base="http://linkedmarkmail.wikier.org", log="linkedmarkmail.log"):
        self.base = base
        self.api = MarkMail("http://markmail.org")
        self.cache = Cache()
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s", filename=log)
        logging.info("Created a new instance of LinkedMarkMail at %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def search(self, query):
        search = self.api.search(query)
        return "" #FIXME

    def get_message(self, key):
        logging.info("Trying to get message %s" % key)
        message = self.api.get_message(key)
        if (message != None):
            url = "%s/message/%s" % (self.base, key)
            post = Post(url, key, message["title"], message["content"])
            triples = len(post)
            if (self.cache.update(post)):
                logging.info("Updated cache of post %s (%d triples)" % (key, triples))
            logging.info("Returning %d triples of post %s" % (triples, key))
            return post.get_data_xml()
        else:
            logging.error("Post %s not found" % key)
            return None

    def get_thread(self, key):
        logging.info("Trying to get thread %s" % key)
        thread = self.api.get_thread(key)
        if (thread != None):
            siocThread = Thread(self.base, key, thread["subject"], thread["permalink"], thread["atomlink"], thread["messages"]["message"])
            triples = len(siocThread)
            if (self.cache.update(siocThread)):
                logging.info("Updated cache of thread %s (%d triples)" % (key, triples))
            logging.info("Returning %d triples of thread %s" % (triples, key))
            return siocThread.get_data_xml()
        else:
            logging.error("Thread %s not found" % key)
            return None


if __name__ == "__main__":
    lmm = LinkedMarkMail()
    #print lmm.get_message("5")
    print lmm.get_message("5wfms7w5opja4a2y")
    #print lmm.get_thread("5")
    #print lmm.get_thread("dcue2bsyrsgbzsd5")


