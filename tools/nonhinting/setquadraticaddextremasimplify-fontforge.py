#!/usr/bin/env python
#
# setquadraticaddextremasimplify-fontforge.py
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
# This program takes a OpenType-CFF font with Cubic (aka PostScript) 
# Outlines and converts them to Quadratic (aka TrueType) outlines,
# and then adds exrema and simplifies all contours to reduce filesize
# and generates a new TTF file

# Import our system library and fontTools ttLib
import sys, fontforge

def main(argv):
#   Open the font file supplied as the first argument on the command line
    font_in = argv[0]
    font = fontforge.open(font_in)

#   Convert all layers to Quadtraic (TTF) form
    font.layers["Fore"].is_quadratic = True

    font.selection.all()

#   Add Extrema
    font.addExtrema()
#   Simplify
    font.simplify(1,('setstarttoextremum','removesingletonpoints'))
#   Correct Directions
    font.correctDirection()


#   Save an SFD
#    font_out = font_in[0:-4] + '-TTF.sfd'
#    font.save(font_out)

#   Generate a TTF
    flags = ('omit-instructions','dummy-dsig','opentype')
    font_out = font_in[0:-4] + '.ttf'
    font.generate(font_out, flags = flags)

if __name__ == '__main__':
    main(sys.argv[1:3])
