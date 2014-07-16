#!/usr/bin/env python
#
# sfd2ttf.py
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
# This program converts a SFD to an TTF
#
# Usage:
#
# $ ./sfd2ttf.py FontIn.sfd

# Import our system and fontforge libraries
import sys, fontforge

def main(argv):

    font_in = argv[0]
#   Check the font file supplied as the first argument on the 
#   command line is an SFD
    if font_in[-3:] == "sfd" or "SFD":
#       Open it
        font = fontforge.open(font_in)
#       Set the output filename correctly
        if font_in[-8:] == "-TTF.sfd":
            font_out = font_in[0:-8] + '.ttf'
        else:
            font_out = font_in[0:-4] + '.ttf'
#       Generate the new TTF with no hinting instructions
        flags = ('omit-instructions',)
        font.generate(font_out, flags = flags)

if __name__ == '__main__':
    main(sys.argv[1:3])
