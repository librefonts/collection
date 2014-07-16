#!/usr/bin/env python
#
# setnonhinting-fonttools.py
#
# Copyright (c) 2011 Khaled Hosny <khaledhosny@eglug.org>
# Copyright (c) 2011 Dave Crossland <dave@understandingfonts.com>
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
#    suggests it should have value 15 for all sizes. 
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
# This script depends on fontTools Python library, available
# in most packaging systems and sf.net/projects/fonttools/ 
#
# Usage:
#
# $ ./setnonhinting-fonttools.py FontIn.ttf FontOut.ttf

# Import our system library and fontTools ttLib
import sys
from fontTools import ttLib
from fontTools.ttLib.tables import ttProgram

# Open the font file supplied as the first argument on the command line
fontfile = sys.argv[1]
font = ttLib.TTFont(fontfile)

# Save a backup
backupfont = fontfile[0:-4] + '-backup-fonttools-prep-gasp' + fontfile[-4:]
# print "Saving to ", backupfont
font.save(backupfont)
print backupfont, "saved."

# Print the Gasp table
if font.has_key('gasp') == 1:
  print "GASP was: ", font["gasp"].gaspRange
else:
  print "GASP wasn't there"

# Print the PREP table
if font.has_key('prep') == 1:
  print "PREP was: ", ttProgram.Program.getAssembly(font["prep"].program)
else:
  print "PREP wasn't there"

# Create a new GASP table
gasp = ttLib.newTable("gasp")

# Set GASP to the magic number
gasp.gaspRange = {65535: 15}

# Create a new hinting program
program = ttProgram.Program()

assembly = ['PUSHW[]', '511', 'SCANCTRL[]', 'PUSHB[]', '4', 'SCANTYPE[]']
program.fromAssembly(assembly)

# Create a new PREP table
prep = ttLib.newTable("prep")

# Insert the magic program into it
prep.program = program

# Add the tables to the font, replacing existing ones
font["gasp"] = gasp
font["prep"] = prep

# Print the Gasp table
print "GASP now: ", font["gasp"].gaspRange

# Print the PREP table
print "PREP now: ", ttProgram.Program.getAssembly(font["prep"].program)

# Save the new file with the name of the input file
newfont = fontfile[0:-4] + '-after-fonttools-prep-gasp' + fontfile[-4:]
font.save(newfont)
print newfont, "saved."