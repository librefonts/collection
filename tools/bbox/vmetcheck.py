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
# vmetcheck.py: A FontForge python script to tell you which vertical 
# metrics of a font to fix
#
# Usage:
#
#   $ vmetcheck.py Font.ttf 2> /dev/null
#   Change WinAscent to 1842
#   Change TypoAscent to 1842
#   Change HHeadAscent to 1842
#   Change WinDescent to 755
#   Change TypoDescent to -755
#   Change HHeadDescent to -755
#   Change TypoLineGap to 0
#   Change HHeadLineGap to 0

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

def main(argv):
    for font_in in argv:
        print font_in,
        font = fontforge.open(font_in)
        print "checked:",
        ymin = 0
        ymax = 0
        for g in fontforge.activeFont().glyphs():
            bbox = g.boundingBox()
            if bbox[3] > ymax: ymax = int(bbox[3])
            if bbox[1] < ymin: ymin = int(bbox[1])
        data = file(font_in, 'rb').read()
        sfnt = Sfnt(data)
        hhea = sfnt.hhea()
        os2 = sfnt.os2()
        if ymax != os2['usWinAscender']: print "Change WinAscent to", ymax
        elif ymax != os2['sTypoAscender']: print "Change TypoAscent to", ymax
        elif ymax != hhea['Ascender']: print "Change HHeadAscent to", ymax
        elif ymin != -os2['usWinDescender']:    print "Change WinDescent to", -ymin
        elif ymin != os2['sTypoDescender']:    print "Change TypoDescent to", ymin
        elif ymin != hhea['Descender']: print "Change HHeadDescent to", ymin
        elif 0 != os2['sTypoLineGap']: print "Change TypoLineGap to 0"
        elif 0 != hhea['LineGap']: print "Change HHeadLineGap to 0"
        else: print "OK"

if __name__ == '__main__':
    main(sys.argv[1:])
