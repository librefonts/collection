#!/usr/bin/env python
#
# setgasp-fontforge.py
#
# Copyright 2011, Google Inc.
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
# This program takes a TTF font sets its GASP table to
# magic value 15 in Version 1 that turn on rendering features that 
# provide optimal font display according to Vern Adams 
# <vern@newtypography.co.uk>
#
# This script depends on the FontForge Python library, available
# in most packaging systems and sf.net/projects/fontforge/ 
#
# Usage:
#
# $ ./setnonhinting-fontforge.py FontIn.ttf [FontOut.ttf]

# Import our system library and fontTools ttLib
import sys, fontforge

def getgasp(font):
    prepAsm = font.getTableData("prep")
    prepText = fontforge.unParseTTInstrs(prepAsm)
    return prepText

def main(argv):
#   Open the font file supplied as the first argument on the command line
    font_in = argv[1]
    font = fontforge.open(font_in)
#   If there is a second font file specified on the command line, output to that
    if argv[2]:
        font_out = argv[2]
#   Else, update the file
    else:
        font_out = font_in

#   Print the existing PREP table
    print "The GASP table is:"
    gasp = font.gasp()
    print gasp

#   Set PREP to magic prep
# TODO FINISH FROM HERE
    magicgasp = "masgic"
    font.gasp = fontforge.parseTTInstrs(prepTextMagic)
    font.setTableData("prep",prepAsmMagic)

#   Print the existing PREP table
    print "The PREP table is now:"
    print getprep(font)

#   Generate the new font with no hinting instructions
    flags = ('omit-instructions',)
    font.generate(font_out, flags = flags)

if __name__ == '__main__':
    main(sys.argv)

font = ttLib.TTFont()

# Open the GASP table
gasp = font["gasp"]

# Set the GASP table
gasp.gaspRange = {65535: 15}

# Set the PREP table

# prep = font["prep"]
# assembly = ['PUSHW[]', '511', 'SCANCTRL[]', 'PUSHB[]', '4', 'SCANTYPE[]']
# prep.program.fromAssembly(assembly)

# Save the font to the filename supplied as the second 
# argument on the command line

font.save(sys.argv[2])


