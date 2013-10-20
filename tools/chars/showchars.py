#!/usr/bin/python

# Copyright 2010, Google Inc.
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
# chars.py: A FontForge python script for printing unicode points and
# glyph names in a font
#
#   unicodepoint glyphname
#
# Usage:
#
#   $ python chars.py Font.ttf 2> /dev/null
#   0x0061 a
#   0x0062 b
#   0x0063 c

import fontforge, sys

def main(argv):
    font_in = argv[0]
    font = fontforge.open(font_in)
    for g in fontforge.activeFont().glyphs():
        print "0x%0.4X" % fontforge.unicodeFromName(g.glyphname), g.glyphname

if __name__ == '__main__':
    main(sys.argv[1:2])
