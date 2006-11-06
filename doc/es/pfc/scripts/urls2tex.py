#!/usr/bin/env python2.4
#
# Copyright (C) 2006 Sergio Fdez, Ivan Frade
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

import HTMLParser
import urllib

try:
	import tidy
	tidy_loaded = True
except ImportError:
	tidy_loaded = False
	print "Unable to load tidy"

class html(HTMLParser.HTMLParser):

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self._title = ""
        self.inTitle = False

    def handle_starttag(self, tag, attrs):
				if ( tag == "title" ):
						self.inTitle = True

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.inTitle:
            self._title = data
        self.inTitle = False

    def get_title(self):
        return self._title.strip()

options = dict(output_xhtml=1, 
                add_xml_decl=1, 
                indent=1, 
                tidy_mark=0,
				quote_nbsp=1,
				quote_ampersand=1,
				escape_cdata=1)

def getTitleFromURL(url):
	f = urllib.urlopen(url)
	s = f.read()
	if tidy_loaded:
		s =str(tidy.parseString(s, **options))
	
	myparser =html()
	try:
		myparser.feed(s)
		return myparser.get_title()
	except HTMLParser.HTMLParseError:
		return ''
			


import os, sys, re

def getFiles(base, listFiles, ext=None):
	for root, dirs, files in os.walk(base):
		for name in dirs:
			listFiles = getFiles(os.path.join(root,name), listFiles, ext)
		for name in files:
			path = os.path.join(root,name);
			if (not '/.svn/' in path) and (not path in listFiles):
				if (ext == None):
					listFiles.append(path)
				else:
					if (path[-len(ext):] == ext):
						listFiles.append(path)
	return listFiles
	
def parseUrls(source):
	urls = []
	pattern = re.compile('\\url{http://[^+]*?}')
	try:
		for line in open(source):
			results = pattern.finditer(line)
			for result in results:
				url = result.string[result.start()+4:result.end()-1]
				urls.append(url)
	except IOError, details:
		print 'Problem reading from ' + source + ': ' + str(details)
	return urls

def getUrls(base):
	files = []
	files = getFiles(base, files, '.tex')
	urls = []
	for path in files:
		for url in parseUrls(path):
			if not url in urls:
				urls.append(url)
	return urls
	

if __name__ == '__main__':

	try:
		   
		if (len(sys.argv)>1):
			base = sys.argv[1]
			urls = getUrls(base)
			for url in urls:
				title = getTitleFromURL(url)
				print ' - ' + title + '\n\t<' + url + '>'
		else:
			sys.exit()
                        
	except KeyboardInterrupt:
		print 'Received Ctrl+C or another break signal. Exiting...'
		sys.exit()
