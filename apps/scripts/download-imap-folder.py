#!/usr/bin/python
# -*- coding: utf8 -*-
#
# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2008 Sergio Fernández
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

"""Script to get the messages stored in a IMAP folder"""

import sys
import logging
import imaplib

class IMAPFolder:

    def __init__(self, host, user, password, folder):
        self.host = host
        self.user = user
        self.password = password
        self.folder = folder

        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s", stream=sys.stdout)        

        try:
            self.imap = imaplib.IMAP4(self.host)
            logging.info("Initializated IMAPFolder")
        except Exception, e:
            logging.error("Error initilizating IMAPFolder: %s" % e[1])
            sys.exit(-1)

    def get(self):
        try:
            self.imap.login(self.user, self.password)
        except Exception, e:
            logging.error("Error trying to login: %s" % str(e))
            sys.exit(-1)
        
        status, data = self.imap.select(self.folder, "readonly")
        if status != "OK":
            logging.error("Error selecting '%s': %s" % (self.folder, data[0]))
        else:
            mbox = ""
            #FIXME: read
            if (len(mbox)>0):
                self.save(mbox, host+"-"+self.folder.replace("/", "-")[-1]+".mbox")
            else:
                logging.error("No data to save, aborted")
            self.imap.close()  
        self.imap.logout()

    def save(self, data, path):
        try:
            f = open(path, "w+")
            f.write(data)
            f.flush()
            f.close()
            logging.info("Folder exported to '%s' file" % path)
        except IOError, detail:
            logging.error("Error writting to disk: %s" % str(detail))

def usage():
    print """
    Usage:
        python download-imap-folder.py host username password folder

    """
    sys.exit(-1)

if __name__ == "__main__":
    try:
        args = sys.argv[1:]
        if (len(args)<4):
            usage()
        else:
            imapfolder = IMAPFolder(args[0], args[1], args[2], args[3])
            imapfolder.get()
    except KeyboardInterrupt:
        print "Received Ctrl+C or another break signal. Exiting..."

