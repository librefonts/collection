# checkout Google Font Directory:
# $ hg clone https://code.google.com/p/googlefontdirectory/ 
# 
# activate font bakery virtualenv or make different with FontTools installed:
# $ source /Users/xen/Dev/font/bakery/venv/bin/activate
# ttx command should work
#
# run this script inside of mercurial clone root
# this script get only one parameter TOKEN
# curl -i -u xen -d '{"scopes":["repo"]}' https://api.github.com/authorizations
# change xen to your GitHub user name, make sure you are have access to 
# fontdirectory organization on GitHub.
# !!!!!!! Don't share your token to anyone, it is very unsecure. 

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
# for f in {apache,ofl,ufl}; do
for f in ./ufl/*; do
    cd $f
    # with license in name
    # name=$(echo $f | sed "s/.\///" | sed "s/\//-/")

    # only name
    license=$(echo $f|sed)
    name=$(echo $f | sed 's/.*\///')
    echo "curl -H \"Authorization: token $TOKEN\" -d '{\"name\":\"$name\"}' -X POST https://api.github.com/orgs/fontdirectory/repos"
    # curl -H "Authorization: token $TOKEN" -d '{"name":"$name"}' -X POST https://api.github.com/orgs/fontdirectory/repos 
    find . -name "*.ttf" -exec ttx {} \;
    find . -name "*.ttf" -exec rm -rf {} \;
    # copy template folders data
    rsync -av $TEMPLATE . --exclude=.git
    git init
    git add .
    git commit -m "Move font files to separate repository from https://code.google.com/p/googlefontdirectory/"
    echo "git remote add origin git@github.com:testfontdirectory/$name.git"
    git remote add origin git@github.com:testfontdirectory/$name.git
    git push -u origin master
    cwd=$(pwd)
    cd $ALL/$license
    git submodule add git://github.com/fontdirectory/$name.git $name
    cd $cwd
    # # echo "curl -H \"Authorization: token $TOKEN\" -d '{\"name\":\"$name\"}' -X POST https://api.github.com/orgs/fontdirectory/repos"
    # # echo "git remote add origin git@github.com:testfontdirectory/$name.git"
    cd ../../
done

# to activate this hg extension http://mercurial.selenic.com/wiki/PurgeExtension
# hg purge
