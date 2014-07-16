#!/usr/bin/env python
#
# setnonhinting-fontforge.py
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
# This program takes a TTF font with no hinting and sets
# its hinting tables with magic values that turn on 
# rendering features that provide optimal font display. 
#
# The magic is in two places: 
#
# 1. The GASP table. Vern Adams <vern@newtypography.co.uk>
#    suggests it should have value 15 for all sizes, which
#    means turning everything on.
#
# 2. The PREP table. Raph Levien <firstname.lastname@gmail.com>
#    suggests using his code to turn on 'drop out control'
#
# PUSHW_1
#  511
# SCANCTRL
# PUSHB_1
#  4
# SCANTYPE
#
# This script depends on the FontForge Python library, available
# in most packaging systems and sf.net/projects/fontforge/ 
#
# Usage:
#
# $ ./setnonhinting-fontforge.py FontIn.ttf [FontOut.ttf]

# Import our system library and fontTools ttLib
import sys, fontforge

def main(argv):
#   Open the font file supplied as the first argument on the command line
    font_in = argv[0]
    font = fontforge.open(font_in)

    font.

#   If there is a second font file specified on the command line, output to that
    if len(argv) == 2:
        font_out = argv[1]
#   Else, update the file
    else:
        font_out = font_in
#   If we opened a SFD, save it
    if font_in[-3:] == "sfd" or "SFD":
        font.save(font_out)
#   Else if we opened a TTF, generate the new font with no hinting instructions
    if font_in[-3:] == "ttf" or "TTF" or "otf" or "OTF":
        flags = ('omit-instructions',)
        font.generate(font_out, flags = flags)

if __name__ == '__main__':
    main(sys.argv[1:3])
