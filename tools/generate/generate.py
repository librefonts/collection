#!/usr/bin/python
# 
# Copyright 2010, Understanding Limited.
# Author: Dave Crossland (dave@understandinglimited.com)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# A script for generating fonts using FontForge.

def usage():
    print """
Usage: generate.py [-h] [--otf] [--ttf] FontIn.sfd [FontOut.ext]

Generate a font.

Required arguments:

 FontIn.sfd     SFD file input

Optional arguments:

 -h, --help      show this help message and exit

 -o, --otf       output a OpenType file

 -t, --ttf       output a TrueType file
 
 -s, --simplifiedotf output a OpenType file, simplified

 FontOut.ext     specify the name of the output file, and 
                 determine type from file extension
"""

import sys, os, getopt, fontforge

def gen(f, type):
    if type == "ttf":
            font_out = f.fontname + '.ttf'
            print "TTF", font_out,
            # 2010-12-10 this should convert layers to quadratic
            f.generate(font_out)
            print "done."
    if type == "otf":
            font_out = f.fontname + '.otf'
            print "OTF", font_out,
            f.generate(font_out)
            print "done."
    if type == "sotf":
            font_out = f.fontname + '.otf'
            print "OTF", font_out,
            # Add Extrema
            f.addExtrema()
            # Simplify
            f.simplify(1,('setstarttoextremum','removesingletonpoints'))
            # Correct Directions
            f.correctDirection()
            f.generate(font_out)
            print "done."


def main(argv):
    try:                                
        optlist, args = getopt.gnu_getopt(argv, 'oths', ['otf', 'ttf', 'help', 'simplifiedotf'])
    except getopt.GetoptError, err: 
        print str(err)
        usage()
        sys.exit(2)
    font_in = args[0]
    f = fontforge.open(font_in)
    print "Opened", f.fontname
    if len(args) == 2:
        font_out = args[1]
        print "Outputting", font_out,
        f.generate(font_out)
        print "done."
        sys.exit()
    for opt, oarg in optlist:
        if opt in ("-h", "--help"):
            print "Help"
            usage()
            sys.exit()
        if opt in ("-t", "--ttf"):
            gen(f, "ttf")
            sys.exit()
        if opt in ("-o", "--otf"):
            gen(f, "otf")
            sys.exit()
        if opt in ("-s", "--simplifiedotf"):
            gen(f, "sotf")
            sys.exit()
    gen(f, "ttf")
    gen(f, "otf")
    
if __name__ == '__main__':
    main(sys.argv[1:])
