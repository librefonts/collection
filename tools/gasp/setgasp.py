#! /usr/bin/python

# Copyright 2010, Google Inc.
# Author: Raph Levien (<firstname.lastname>@gmail.com)

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

# Script for setting GASP table in font files. Usage:
#
# python setgasp.py fontfile.ttf <code>

# Note: this requires a recent devel version of the FontForge libs, because
# of a bug in set_gasp.

import fontforge
import sys
import os
import re

# Given a short string ("x20xy"), return a FontForge-compatible gasp tuple
def code_to_gasp(code):
  gasp = []
  while code != '':
    m = re.match('(xy?)(\d*)(.*)', code)
    if m:
      if m.group(1) == 'x':
        tup = ('gridfit', 'antialias')
      else:
        tup = ('gridfit', 'antialias', 'symmetric-smoothing', 'gridfit+smoothing')
      if m.group(2) == '':
        if m.group(3) != '':
          print 'Malformed code'
          break
        num = 65535
      else:
        num = int(m.group(2)) - 1
      code = m.group(3)
      gasp.append((num, tup))
    else:
      print 'Malformed code'
      break
  return tuple(gasp)

def gen_with_gasp(font_in, name_out, gasp):
  font = fontforge.open(font_in)
  font.gasp_version = 1
  font.gasp = gasp
  font.generate(name_out)
  font.close()

def main(args):
  font_in, code = args[1:]
  gasp = code_to_gasp(code)
  print 'New gasp table:', gasp
  gen_with_gasp(font_in, font_in, gasp)

if __name__ == '__main__':
  main(sys.argv)
