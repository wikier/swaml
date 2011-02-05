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

from markmail import MarkMail
from swaml import Post

class LinkedMarkMail:

    def __init__(self, base="http://swaml.berlios.de/sandbox/linkedmarkmail"):
        self.base = base
        self.api = MarkMail("http://markmail.org")

    def search(self, query):
        search = self.api.search(query)
        return "" #FIXME

    def get_message(self, key):
        message = self.api.get_message(key)
        url = "%s/post/%s" % (self.base, key)
        post = Post(url, key, message["title"], message["content"])
        return post.get_data_xml()

    def get_thread(self, key):
        thread = self.api.get_thread(key)
        return "" #FIXME


if __name__ == "__main__":
    lmm = LinkedMarkMail()
    print lmm.get_message("5wfms7w5opja4a2y")


