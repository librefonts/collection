#!/usr/bin/python

# Copyright 2010, Google Inc.
# Author: Raph Levien (<firstname.lastname>@gmail.com)
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
# vmet.py: A FontForge python script for printing bounding box
# maximums and the vertical metrics of a font
#
# Usage:
#
#   $ vmet.py Font.ttf 2> /dev/null
#   MaxGlyph      1842.0
#   WinAscent     1842
#   TypoAscent    1440
#   HHeadAscent   1440
#   MinGlyph     -755.0
#   WinDescent    755
#   TypoDescent  -608
#   HHeadDescent -608
#   TypoLineGap   0
#   HHeadLineGap  0

import fontforge, sys, struct

class Sfnt:
    def __init__(self, data):
        version, numTables, _, _, _ = struct.unpack('>IHHHH', data[:12])
        self.tables = {}
        for i in range(numTables):
            tag, checkSum, offset, length = struct.unpack('>4sIII', data[12 + 16 * i: 28 + 16 * i])
            self.tables[tag] = data[offset: offset + length]

    def hhea(self):
        r = {}
        d = self.tables['hhea']
        r['Ascender'], r['Descender'], r['LineGap'] = struct.unpack('>hhh', d[4:10])
        return r

    def os2(self):
        r = {}
        d = self.tables['OS/2']
        r['fsSelection'], = struct.unpack('>H', d[62:64])
        r['sTypoAscender'], r['sTypoDescender'], r['sTypoLineGap'] = struct.unpack('>hhh', d[68:74])
        r['usWinAscender'], r['usWinDescender'] = struct.unpack('>HH', d[74:78])
        return r

def set_os2(name, val):
    print name, val


def main(argv):
    font_in = argv[0]
    font = fontforge.open(font_in)
    ymin = 0
    ymax = 0
    for g in fontforge.activeFont().glyphs():
        bbox = g.boundingBox()
        if bbox[3] > ymax: ymax = bbox[3]
        if bbox[1] < ymin: ymin = bbox[1]
    data = file(font_in, 'rb').read()
    sfnt = Sfnt(data)
    hhea = sfnt.hhea()
    os2 = sfnt.os2()
    print "MaxGlyph     ", ymax
    print "WinAscent    ", os2['usWinAscender']
    print "TypoAscent   ", os2['sTypoAscender']
    print "HHeadAscent  ", hhea['Ascender']
    print "MinGlyph    ", ymin
    print "WinDescent   ", os2['usWinDescender']
    print "TypoDescent ", os2['sTypoDescender']
    print "HHeadDescent", hhea['Descender']
    print "TypoLineGap  ", os2['sTypoLineGap']
    print "HHeadLineGap ", hhea['LineGap']

if __name__ == '__main__':
    main(sys.argv[1:2])