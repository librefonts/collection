#!/usr/bin/python
#
# Copyright 2014, Google Inc.
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
# A script for printing the Unicode chars in a given string
# 
# See also: http://rishida.net/tools/conversion/
#
# $ ~/googlefontdirectory/tools/chars/string.py hello
# h U+0068
# e U+0065
# l U+006c
# l U+006c
# o U+006f
# U+0068 U+0065 U+006c U+006c U+006f
# $

import sys, unicodedata

# print char and code
for i, c in enumerate(sys.argv[1]):
    print c + ' U+%04x' % ord(c)

# print codes all on one line
for i, c in enumerate(sys.argv[1]):
    print 'U+%04x' % ord(c),
