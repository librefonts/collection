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
# namelist.py: A FontForge python script for generating namelist files.
#
# Usage:
#
#   $ python namelist.py Font.ttf NameList.nam

import fontforge

def main(argv):
    font_in, namelist_out = argv
    font = fontforge.open(font_in)
    font.saveNamelist(namelist_out)

if __name__ == '__main__':
    main(sys.argv[1:2])
