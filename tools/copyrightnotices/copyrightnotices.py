#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
#
# Copyright 2012, Google Inc.
# Author: Dave Crossland (dcrossland a google com)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#		 http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# A script for generating a HTML file containing copyright notices 
# for all fonts found in a directory tree, using fontTools

def usage():
	print >> sys.stderr, "copyrightnotices.py /directory/tree/of/fonts/ html_file_to_output_notices_to.html "

# TODO: .decode() doesn't work very well, this should be improved
# TODO make this drop fonts in directories where a METADATA.json if found with Visibility: Internal

# Pseudo Code:
#
# for each font file found in the tree:
#   get its metadata
#
# for each font:
#   print font file name
#   print copyright string
#   print license link

import os, sys, codecs, json
from datetime import date
from fontTools import ttLib

def copyright(string, metadata):
	metadata['Copyright'] = string
	return metadata
def fullname(string, metadata):
	metadata['Full Name'] = string
	return metadata
def version(string, metadata):
	metadata['Version'] = string
	return metadata
def psname(string, metadata):
	metadata['PostScript Name'] = string
	return metadata
def trademark(string, metadata):
	metadata['Trademark'] = string
	return metadata
def manufacturor(string, metadata):
	metadata['Manufacturor'] = string
	return metadata
def designername(string, metadata):
	metadata['Designer'] = string
	return metadata
def description(string, metadata):
	metadata['Font Description'] = string
	return metadata
def vendorurl(string, metadata):
	metadata['Vendor URL'] = string
	return metadata
def designerurl(string, metadata):
	metadata['Designer URL'] = string
	return metadata
def licensedesc(string, metadata):
	metadata['License Description'] = string
	return metadata
def licenseurl(string, metadata):
	metadata['License URL'] = string
	return metadata
def extractMetadata(filename):
	nametable = { 0 : copyright,
		          4 : fullname,
		          5 : version,
		          6 : psname,
		          7 : trademark,
		          8 : manufacturor,
		          9 : designername,
		         10 : description,
		         11 : vendorurl,
		         12 : designerurl,
		         13 : licensedesc,
		         14 : licenseurl,
	}
	metadata = { "Filename" : filename, }
	with open(filename, "rb") as file:
		font = ttLib.TTFont(file)
		for record in font['name'].names:
			try:
				if '\000' in record.string:
					string = unicode(string, 'utf-16-be').encode('utf-8')
				else:
					string = record.string
				# Here is a fancy bit, "use the functions as the values of the dictionary and then call them via dictionary lookup"
				# Explained in http://bytebaker.com/2008/11/03/switch-case-statement-in-python/
				nametable[record.nameID](string, metadata)
			except:
				pass
	return metadata

def createHtml(pathmetadata):
	today = unicode(date.today().strftime("%Y-%m-%d"))
	html = "<html><head><title>Fonts File Copyright Notices %s</title></head><body>" % today
	for path, metadata in sorted(pathmetadata.iteritems()):
		html += "<h4>%s</h4>" % path.rpartition("/")[2]
# This will print all the metadata
#		html += "<dl>"
#		for key, value in sorted(metadata.iteritems()):
#			html += "<dt>%s</dt>" % key
#			html += "<dd>%s</dd>" % value.decode('utf8', 'replace') # This doesn't work very well...
#		html += "</dl>"
# But we just want the copyright and license URLs
		for key, value in metadata.items():
			if key == "Copyright":
				html += "<p>Copyright: %s</p>" % value.decode('utf8', 'replace') # This doesn't work very well...
			elif key == "License URL":
				html += "<p>License: <a href='%s'>%s</a></p>" % (value.decode('utf8', 'replace'), value.decode('utf8', 'replace')) # This doesn't work very well...
	html += "</body></html>"
	return html

def writeFile(htmlfilename, html):
#	check the os.path.exists works
	if os.path.exists(htmlfilename):
		print >> sys.stderr, "File exists:", htmlfilename
		raise Exception
	with codecs.open(htmlfilename, 'w', encoding="utf_8") as f:
		f.write(html)
		print "Created", htmlfilename

def run(path, htmlfilename):
	# get fontfilenames from path's tree
	# TODO make this drop fonts in directories where a METADATA.json if found with Visibility: Internal
	fontfilenames = []
	for root, subFolders, files in os.walk(path):
		if '.hg' in subFolders:
				subFolders.remove('.hg')
		for file in files:
			if file.endswith("ttf"):
				fontfilenames.append(os.path.join(root,file))



	# make a parent dictionary for metadata with filepath as key
	pathmetadata = {}
	for filename in fontfilenames:
		metadata = extractMetadata(filename)
		pathmetadata[filename] = metadata
	# write it out as a html file
	html = createHtml(pathmetadata)
	writeFile(htmlfilename, html)

def main(argv=None):
	if argv is None:
		argv = sys.argv
	if len(argv) != 3:
		usage()
		return 1
	run(argv[1], argv[2])
	return 0

if __name__ == '__main__':
	sys.exit(main())
