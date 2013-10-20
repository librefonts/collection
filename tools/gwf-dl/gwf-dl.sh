#!/bin/bash

# author: Izzy Galvez (iglvzx), i@iglvz.us
# This script checks for updates to the Google Font Directory and copies any new
# or updated *.ttf files to the user's font directory.

# Note: you must have Mercurial (hg) installed, and have already cloned the
# Google Font Directory project to your system. To do this run:
# hg clone https://googlefontdirectory.googlecode.com/hg/ googlefontdirectory;
# where "googlefontdirectory" is the location where you wish to maintain the
# project. (The project is several hundred MB's in size. Be patient.)

# Change these variables to match your current setup.
projdir=~/Mercurial/googlefontdirectory
fontdir=~/.fonts

echo "Project directory: $projdir"
cd $projdir

echo -e "Downloading updates ...\n"
hg pull -u

echo -e "\nFonts directory: $fontdir"
echo -e "Copying *.ttf files to fonts directory ..."
find -name "*.ttf" -exec cp {} -u -v "$fontdir" \;

echo -e "\nUpdating font cache ...\n"
fc-cache -v $fontdir

echo -e "\nDone."