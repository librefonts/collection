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

# Tool for creating HTML preview and interactive selection of GASP table
# settings.
#
# Usage (outputs test.html and support files into current dir):
#
# python gsap-preview.py fontfile.ttf

# Note: this requires a recent devel version of the FontForge libs, because
# of a bug in set_gasp.

import fontforge
import sys
import os

TTF2EOT_BIN = '/home/crossland-fedora14/src/ttf2eot-read-only/ttf2eot'

def gen_with_gasp(font_in, name_out, gasp):
  font = fontforge.open(font_in)
  font.gasp_version = 1
  print font.gasp, font.os2_fstype
  font.gasp = gasp
  #font.os2_fstype = 0
  font.generate(name_out)
  font.close()
  if (name_out.endswith('.ttf')):
    eotfn = name_out[:-4] + '.eot'
    os.system(TTF2EOT_BIN + ' %s > %s' % (name_out, eotfn))

class MakeTest:
  def __init__(self, font_in, fn):
    self.font_in = font_in
    self.fn = fn
    self.tests = []

  def add_test(self, testname):
    x_tup = ('gridfit', 'antialias')
    xy_tup = ('gridfit', 'antialias', 'symmetric-smoothing', 'gridfit+smoothing')
    if testname == 'x':
      gasp = ((65535, x_tup),)
    elif testname == 'xy':
      gasp = ((65535, xy_tup),)
    gen_with_gasp(self.font_in, testname + '.ttf', gasp)
    self.tests.append((testname,))

  def finish(self):
    lo, hi = 6, 37
    fo = file(self.fn, 'w')
    print >> fo, "<!DOCTYPE html>"
    print >> fo, "<html>"
    print >> fo, "  <head>"
    print >> fo, """<script>
function init(_lo, _hi, _fontname) {
  lo = _lo;
  hi = _hi;
  fontname = _fontname;
  state = {};
  for (var i = lo; i < hi; i++) {
    state[i] = '';
  }
  state[lo] = 'xy';
}

function decorate() {
  var defstate = 'x';
  var code = state[lo] == 'xy' ? 'xy' : 'x';
  var lastcode = code;
  for (var i = lo; i < hi; i++) {
    if (state[i] == '') {
      var xstate = (defstate == 'x') ? 'defsel' : 'nosel';
      var xystate = (defstate == 'xy') ? 'defsel' : 'nosel';
    } else {
      defstate = state[i];
      var xstate = (defstate == 'x') ? 'sel' : 'nosel';
      var xystate = (defstate == 'xy') ? 'sel' : 'nosel';
    }
    if (lastcode != defstate) {
      code += i + defstate;
      lastcode = defstate;
    }
    var cellx = document.getElementById('cellx' + i);
    if (cellx) cellx.className = xstate;
    var cellxy = document.getElementById('cellxy' + i);
    if (cellxy) cellxy.className = xystate;
  }
  var cmd = 'python setgasp.py ' + fontname + ' ' + code;
  document.getElementById('cmd').innerHTML = cmd;
}

function doclick(size, val) {
  if (state[size] == val) {
    state[size] = '';
  } else {
    state[size] = val;
  }
  decorate();
}
"""
    print >> fo, "window.onload = function() {"
    print >> fo, "  init(%d, %d, '%s')" % (lo, hi, self.font_in)
    print >> fo, "  decorate()"
    print >> fo, "}"
    print >> fo, "</script>"
    print >> fo, "    <style>"
    print >> fo, "    td { margin: 0px 10px; overflow: hidden; white-space: nowrap; }"
    print >> fo, "    tr { margin: 0px 0px; }"
    print >> fo, "    td.sel { background-color: #ffffb0; }"
    print >> fo, "    td.defsel { background-color: #ffffe0; }"
    print >> fo, "    td.nosel { background-color: #ffffff; }"
    print >> fo, "    table { table-layout: fixed; }"
    for testname, in self.tests:
      print >> fo, "      @font-face {"
      print >> fo, "        font-family: test%s;" % testname
      print >> fo, "        src: url('%s.eot');" % testname
      print >> fo, "        src: local('@'), url('%s.eot') format('embedded-opentype'), url('%s.ttf') format('truetype');" % (testname, testname)
      print >> fo, "      }"
    print >> fo, "    </style>"
    print >> fo, "  </head>"
    print >> fo, "  <body>"
    print >> fo, "  <table width='100%' id='maintable'>"
    for px in range(6, 37):
      print >> fo, "    <tr>"
      print >> fo, "    <td width='20'>%d</td>" % px
      for testname, in self.tests:
        id = 'cell%s%d' % (testname, px)
        clickfn = 'doclick(%d, "%s")' % (px, testname)
        print >> fo, "      <td id='%s' class='nosel' style='font-family:test%s; font-size: %dpx' onclick='%s'>" % (id, testname, px, clickfn)
        print >> fo, "        TOEG The quick brown fox jumps over the lazy dog.</span>"
        print >> fo, "      </td>"
      print >> fo, "    </tr>"
    print >> fo, "    </table>"
    print >> fo, "  <p>Command to set gasp table:</p>"
    print >> fo, "  <pre id='cmd'>"
    print >> fo, "  (Javascript doesn't seem to be working)"
    print >> fo, "  </pre>"
    print >> fo, "  <p>This test page automatically produced by <a href='gasp-preview.py'>gasp-preview.py</a>.</p>"
    print >> fo, "  </body>"
    print >> fo, "</html>"

def main(args):
  font_in = args[1]
  test = MakeTest(font_in, 'test.html')
  test.add_test('x')
  test.add_test('xy')
  test.finish()
  os.system('chmod a+r *')

if __name__ == '__main__':
  main(sys.argv)
