#!/usr/bin/python

# Copyright (c) 2011 Dave Crossland (dave@understandinglimited.com)
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
# prepcheck.py: A FontForge python script for printing the prep table
#
# Usage:
#
#   $ prepcheck.py Font.ttf
#   PUSHW_1
#    511
#   SCANCTRL
#   PUSHB_1
#    4
#   SCANTYPE
#   $

import fontforge, sys

def main(argv):
    font_in = argv[0]
    font = fontforge.open(font_in)
    prepAsm = font.getTableData("prep")
    prepText = fontforge.unParseTTInstrs(prepAsm)
    print prepText

if __name__ == '__main__':
    main(sys.argv[1:2])