#!/usr/bin/env python2.4
# -*- coding: utf8 -*-
#
# Script to make a TeX list of URL's written in another TeX files
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

import os, sys, re
import HTMLParser, urllib

try:
	import tidy
	tidy_loaded = True
except ImportError:
	tidy_loaded = False
	print 'Unable to load tidy'


class HTML(HTMLParser.HTMLParser):

	def handle_starttag(self, tag, attrs):
		if ( tag == 'title' ):
			self.inTitle = True

	def handle_endtag(self, tag):
		pass

	def handle_data(self, data):
		if self.inTitle:
			self._title = data
		self.inTitle = False

	def get_title(self):
		return self._title.strip()

	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self._title = 'FIXME'
		self.inTitle = False


class TeX:

	def getFiles(self, base, listFiles, ext=None):
		for root, dirs, files in os.walk(base):
			for name in dirs:
				listFiles = self.getFiles(os.path.join(root,name), listFiles, ext)
			for name in files:
				path = os.path.join(root,name);
				if (not '/.svn/' in path) and (not path in listFiles):
					if (ext == None):
						listFiles.append(path)
					else:
						if (path[-len(ext):] == ext):
							listFiles.append(path)
		return listFiles
	
	def parseUrls(self, source):
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

	def getUrls(self, base):
		files = []
		files = self.getFiles(base, files, '.tex')
		urls = []
		for path in files:
			for url in self.parseUrls(path):
				if not url in urls:
					urls.append(url)
		return urls


class Urls2TeX:

	def getTitleFromURL(self, url):
		#print '\ntrying with', url,

		try:
			f = urllib.urlopen(url)
		except:
			return 'FIXME'

		s = f.read()
		if tidy_loaded:
			s = str(tidy.parseString(s, **options))
	
		html = HTML()
		try:
			html.feed(s)
			return html.get_title()
		except HTMLParser.HTMLParseError:
			return 'FIXME'

	def loadTranslation(self):
		self.translation = {}

		if (os.path.exists(self.translationFile)):
			try:
				for line in open(self.translationFile):
					line = line.split(' ')
					url = line[0]
					title = ' '.join(line[1:])
					self.translation[url] = title
			except IOError, details:
				print 'Problem reading translation cache: ' + str(details)
		else:
			print 'no initial URL\'s cache founded'
			print 'then this will take some time... be pacient'

	def dump(self):
		self.dumpTex()
		self.dumpTranslation()

	def dumpTex(self):
		try:
			import codecs
			f = open(self.destinationFile, 'w')
			f.write('\n')
			f.write('\\chapter{Referencias}\n')
			f.write('\n')
			f.write('\\begin{itemize}\n')

			for url in self.translation.keys():
				title = self.translation[url]
				f.write(' \\item ' + title + ' <\url{' + url + '}>\n')

			f.write('\\end{itemize}')
			f.write('\n')
			f.close()
			print 'dumped URLs in', self.destinationFile
		except IOError, details:
			print 'Problem writing translation cache: ' + str(details)

	def dumpTranslation(self):
		try:
			f = open(self.translationFile, 'w')
			for url in self.translation.keys():
				title = self.translation[url]
				f.write(url + ' ' + title + '\n')
			f.close()
			print 'dumped URL\'s cache in', self.translationFile
		except IOError, details:
			print 'Problem writing translation cache: ' + str(details)


	def __init__(self, base):
		self.translationFile = 'urls.cache'
		self.destinationFile = 'anexos/referencias.tex'
		self.base = base
		self.loadTranslation()
		self.tex = TeX()

		urls = self.tex.getUrls(self.base)
		for url in urls:
			if not url in self.translation:
				title = self.getTitleFromURL(url)
				if (title != 'FIXME'):
					#print ';', title
					self.translation[url] = title

		self.dump()

	

options = dict(output_xhtml=1, 
				add_xml_decl=1, 
                indent=1, 
                tidy_mark=0,
				quote_nbsp=1,
				quote_ampersand=1,
				escape_cdata=1)


if __name__ == '__main__':

	try:
		   
		if (len(sys.argv)>1):
			Urls2TeX(sys.argv[1])
		else:
			sys.exit()
                        
	except KeyboardInterrupt:
		print 'Received Ctrl+C or another break signal. Exiting...'
		sys.exit()
