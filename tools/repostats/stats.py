# stats - get stats on the given repo
# From # http://www.selenic.com/repo/python-hglib/file/tip/examples/stats.py
#
# Copyright (c) Matt Mackall <mpm@selenic.com>
# Copyright (c) Dave Crossland <dave@understandinglimited.com>
# MIT license @ http://www.selenic.com/repo/python-hglib/file/tip/LICENSE

import sys
import hglib

# figure out what repo path to use
repo = '.'
if len(sys.argv) > 1:
    repo = sys.argv[1]

# connect to hg
client = hglib.open(repo)

# gather some stats
revs = int(client.tip().rev)
files = len(list(client.manifest()))
heads = len(client.heads())
branches = len(client.branches())
tags = len(client.tags()) - 1 # don't count tip

authors = {}
for e in client.log():
    authors[e.author] = True

merges = 0
for e in client.log(onlymerges=True):
    merges += 1

print "%d revisions" % revs
print "%d merges" % merges
print "%d files" % files
print "%d heads" % heads
print "%d branches" % branches
print "%d tags" % tags
print "%d authors" % len(authors)
