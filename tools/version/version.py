#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2012, Google Inc.
#
# Contribtor: Jeremie Lenfant-Engelmann (jeremiele a google com)
# Contribtor: Dave Crossland (dcrossland a google com )
# Contribtor: Mikhail Kashkin (mkashkin a gmail.com)
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
# A script for printing the Version string of fonts in a given directory, using fontTools.

from __future__ import print_function
from __future__ import unicode_literals

from datetime import date
from fontTools import ttLib

import io
import json
import os
import sys
import gzip

if sys.version < '3':
    import codecs
    def u(x):
        if not x:
            return ''
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x

def usage():
    print("version.py family_directory", file=sys.stderr)


def fontToolsOpenFont(filepath):
    f = io.open(filepath, 'rb')
    return ttLib.TTFont(f)

def fontToolsGetVersion(ftfont):
    NAMEID_VERSION = 5
    version = False
    for record in ftfont['name'].names:
        if record.nameID == NAMEID_VERSION and not version:
            if b'\000' in record.string:
                version = record.string.decode('utf-16-be').encode('utf-8')
            else:
                version = record.string
            break
    if not version:
        version = "Unknown"
    return version


def run(familydir):
    fonts = []
    files = os.listdir(familydir)
    for f in files:
        if f.endswith(".ttf"):
            filepath = os.path.join(familydir, f)
            ftfont = fontToolsOpenFont(filepath)
            v = u(fontToolsGetVersion(ftfont))
            print(f + ":", v)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    if len(argv) != 2:
        usage()
        return 1
    run(argv[1])
    return 0

if __name__ == '__main__':
    sys.exit(main())
