#!/usr/bin/env python
#
# ttf2sfd.py
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
# This program converts an OTF to an SFD 
#
# Usage:
#
# $ ./otf2sfd.py FontIn.ttf

# Import our system and fontforge libraries
import sys, fontforge

def main(argv):
#   Open the font file supplied as the first argument on the command line
    font_in = argv[0]
    font = fontforge.open(font_in)

#   Save an SFD
    font_out = font_in[0:-4] + '-OTF.sfd'
    font.save(font_out)

if __name__ == '__main__':
    main(sys.argv[1:3])
