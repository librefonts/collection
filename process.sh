#!/bin/bash
# checkout Google Font Directory:
# $ hg clone https://code.google.com/p/googlefontdirectory/ 
# 
# activate font bakery virtualenv or make different with FontTools installed:
# $ source /Users/xen/Dev/font/bakery/venv/bin/activate
# ttx command should work
#
# run this script inside of mercurial clone root
# this script get only one parameter TOKEN
# curl -i -u xen -d '{"scopes":["repo"], "note":"fontdirectory process.sh"}' https://api.github.com/authorizations
# change xen to your GitHub user name, make sure you are have access to 
# fontdirectory organization on GitHub.
# !!!!!!! Don't share your token to anyone, it is very unsecure. 

# probably you want to activate this hg extension http://mercurial.selenic.com/wiki/PurgeExtension
# and cleanup changes. 
# Don't forget to push all repository after process is done 

if [ $# -eq 0 ]; then
    echo "No arguments supplied, read source please."
    exit 1
fi

TOKEN=$1 
# make sure you run inside of virtualenv with available ttx
TTX="ttx"
# full path only
TEMPLATE="/Volumes/Fonts/template/"
ALL="/Volumes/Fonts/all"
startwd=$(pwd)
# echo "Delete files"
find . \( -name "*.menu" -o -name "*.latin" -o -name "*.latin-ext" -o -name "*.greek" \
-o -name "*.greek-ext" -o -name "*.cyrillic" -o -name "*.cyrillic-ext" -o -name \
"*.vietnamese" -o -name "*.arabic" -o -name "*.bengali" -o -name "*.ethiopic" -o -name \
"*.tamil" -o -name "*.thai" -o -name "*.devanagari" -o -name "*.hebrew" -o -name \
"*.khmer" -o -name "*.lao" \) -exec rm -rf {} \;
# echo "Generate ttx files"
# find . -name "*.ttf" -exec ttx -s -o {}.ttx {} \;
# find . -name "*.otf" -exec ttx -s -o {}.ttx {} \;
# find . -name "*.ttf" -exec rm -rf {} \;
# find . -name "*.otf" -exec rm -rf {} \;

#for f in {apache,ofl,ufl}/*; do
for f in {ofl,apache}/*; do
    echo $startwd/$f 
    cd $startwd/$f
    # only name
    name=$(echo $f | sed 's/.*\///')
    license=$(echo $f | sed 's/.\///' | sed 's/\/.*//')
    # echo "Process $name"
    # echo "curl -H \"Authorization: token $TOKEN\" -X DELETE https://api.github.com/repos/fontdirectory/$name" | bash
    echo "curl -H \"Authorization: token $TOKEN\" -d '{\"name\":\"$name\"}' -X POST https://api.github.com/orgs/fontdirectory/repos" | bash
    git init
    git add .
    git commit -m "Move $name font files to separate repository"
    git remote add origin git@github.com:fontdirectory/$name.git
    git push -u origin master
    cd $ALL
    git submodule add -f git://github.com/fontdirectory/$name.git $f
done

# hg revert --all
# hg purge
