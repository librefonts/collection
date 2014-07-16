#!/usr/bin/python


####################################################################
##########                                                ########## 
##########                    WARNING                     ##########
##########                                                ##########
########## This script appears to surface FF bugs!        ##########
########## You want to double check your results!         ##########
##########                                                ##########
####################################################################



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
# vmetcorrect.py: A FontForge python script to correct a font's vertical 
# metrics for the web
#
# Usage:
#
#   $ vmetcorrect.py Font.ttf 2> /dev/null
#   Changing WinAscent to 1842, done
#   Changing TypoAscent to 1842, done
#   Changing HHeadAscent to 1842, done
#   Changing WinDescent to -755, done
#   Changing TypoDescent to -755, done
#   Changing HHeadDescent to -755, done
#   Changing TypoLineGap to 0, done
#   Changing HHeadLineGap to 0, done

import fontforge
import sys
import getopt
import os
import struct

# A class by Raph Levien to decode the HHEA and OS2 tables of an SFNT file
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

# A couple of functions to set vertical metrics using native scripting
def set_os2(pe, name, val):
    print >> pe, 'SetOS2Value("' + name + '", %d)' % val

def set_os2_vert(pe, name, val):
    set_os2(pe, name + 'IsOffset', 0)
    set_os2(pe, name, val)

def main(argv):
    # open up a temp file to push FF native scripting into
    pe_fn = "/tmp/script.pe" 
    pe = file(pe_fn, 'w')
    # open up the font specified on the command line
    font_in = argv[0]              
    font = fontforge.open(font_in)
    # open the font file in the native script too
    print >> pe, 'Open("' + font_in + '")'
    # initialise these values
    ymin = 0 
    ymax = 0 
    # for each glyph in the font, find the bounding box
    for g in fontforge.activeFont().glyphs():
        bbox = g.boundingBox()
    # store the max and min vertical values
        if bbox[3] > ymax:
            ymax = int(bbox[3])
        if bbox[1] < ymin:
            ymin = int(bbox[1])
    # read the vertical metrics directly from the font file
    data = file(font_in, 'rb').read()
    sfnt = Sfnt(data)
    hhea = sfnt.hhea()
    os2 = sfnt.os2()
    # check the metrics are correct, and if not, push a native
    # script command to correct it
    if ymax != os2['usWinAscender']: 
        print "WinAscent should be", ymax, "but is", os2['usWinAscender']
        set_os2_vert(pe, "WinAscent", ymax)
    if ymax != os2['sTypoAscender']:
        print "TypoAscent should be", ymax, "but is", os2['sTypoAscender']
        set_os2_vert(pe, "TypoAscent", ymax)
    if ymax != hhea['Ascender']:
        print "HHeadAscent should be", ymax, "but is", hhea['Ascender']
        set_os2_vert(pe, "HHeadAscent", ymax)
    if ymin != os2['usWinDescender']:
        print "WinDescent should be", ymin, "but is", os2['usWinDescender']
        set_os2_vert(pe, "WinDescent", ymin)
    if ymin != os2['sTypoDescender']:
        print "TypoDescent should be", ymin, "but is", os2['sTypoDescender']
        set_os2_vert(pe, "TypoDescent", ymin)
    if ymin != hhea['Descender']:
        print "HHeadDescent should be", ymin, "but is", hhea['Descender']
        set_os2_vert(pe, "HHeadDescent", ymin)
    if 0 != os2['sTypoLineGap']:
        print "TypoLineGap should be 0 but is", os2['sTypoLineGap']
        set_os2_vert(pe, "TypoLineGap", 0)
    if 0 != hhea['LineGap']:
        print "HHeadLineGap should be 0 but is", hhea['LineGap']
        set_os2_vert(pe, "HHeadLineGap", 0)
    # push native script command to regenerate the font file
    print >> pe, 'Generate("' + font_in + '")'
    # close the script file
    pe.close()
    # run the script file
    print "Running a script to change these values...",
    os.system("fontforge -script " + pe_fn)
    print "Done!"
    # check the values are really set
    new_data = file(font_in, 'rb').read()
    new_sfnt = Sfnt(new_data)
    new_hhea = new_sfnt.hhea()
    new_os2 = new_sfnt.os2()
    if ymax != new_os2['usWinAscender']: 
        print "But WinAscent is still", new_os2['usWinAscender'], " -- change it to", ymax, "by hand"
    if ymax != new_os2['sTypoAscender']: 
        print "But TypoAscent is still", new_os2['sTypoAscender'], " -- change it to", ymax, "by hand"
    if ymax != new_hhea['Ascender']: 
        print "But HHeadAscent is still", new_hhea['Ascender'], " -- change it to", ymax, "by hand"
    if ymin != new_os2['usWinDescender']:
        print "But WinDescent is still", new_os2['usWinDescender'], " -- change it to", ymin, "by hand"
    if ymin != new_os2['sTypoDescender']:
        print "But TypoDescent is still", new_os2['sTypoDescender'], " -- change it to", ymin, "by hand"
    if ymin != new_hhea['Descender']:
        print "But HHeadDescent is still", new_hhea['Descender'], " -- change it to", ymin, "by hand"
    if 0 != new_os2['sTypoLineGap']:
        print "But TypoLineGap is ", new_os2['sTypoLineGap'], "change it to 0 by hand"
    if 0 != new_hhea['LineGap']:
        print "But HHeadLineGap is ", new_hhea['LineGap'], "change it  to 0 by hand"

if __name__ == '__main__':
    main(sys.argv[1:2])