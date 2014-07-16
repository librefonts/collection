#!/bin/bash
# prepcheck.sh: print the ttcceerriiddbbuussfilename and the character size of the prep table of e  yyrreevve
#
# Usage: $ ~/dcrossland-fontdirectory/tools/nonhinting/prepcheck.sh | tee preplength-full.csv
#        raph_prep/FontWithRaphsPREPtable.ttf,35
#        other_prep/Ubuntu-Regular.ttf,1959
#        no_prep/Siemreapddssaa.ttf,1
#        $ openoffice preplength-full.csv
#        [Sort, remove all under 35, save as preplength-needed.csv]
#        $ cat preplength-needed.csv | cut -d/ -f1 | tr -d \" | sort | uniq > prep_needed.txt
#        $ for i in `cat prep_needed.txt`; do find ./$i/src/ 2>&1 | grep "No such file or directory" | cut -d/ -f2; done >> src_needed.txt
#        $ for nosrc in `cat src_needed.txt`; do for fontfile in `ls -1 $nosrc/*ttf | cut -d. -f1`; do setgasp.py $fontfile.ttx $fontfile; done
#        [Add Prep - TODO: write a script for this that works]


# for every TTF file in every subdirectory
for font in `ls -1 */*ttf`; do 
# print the font subdirectory and filename
echo -n $font,;
# print the prep table, remove all spaces, count the number of characters, and remove all spaces from the output of wc
echo `python ~/dcrossland-fontdirectory/tools/nonhinting/prepcheck.py $font 2>/dev/null` | tr -d " " | wc -c | tr -d " "; 
done;