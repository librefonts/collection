#!/bin/bash
#
# showttf Font.ttf | grep -E '(scen|gap|(HHEAD|OS/2) table)'
#
echo $1;
echo "Ascent metrics should be the ";
echo -n "bbox "; showttf $1 | grep ymax= | tr -d "\t " | tr "=" "\t" ;
echo ""
showttf $1 | grep usWinAscent= | tr -d "\t " | tr "=" "\t" ;
# captured in following grep
# showttf $1 | grep stypeascender= | tr -d "\t " | tr "=" "\t" ;
showttf $1 | grep ascender= | tr -d "\t " | tr "=" "\t" ;
echo ""

echo "Descent metrics should be the ";
echo -n "bbox "; showttf $1 | grep ymin= | tr -d "\t " | tr "=" "\t" ;
echo ""
echo "(WinDescent should be positive)"
showttf $1 | grep usWinDescent= | tr -d "\t " | tr "=" "\t" ;
# captured in following grep
# showttf $1 | grep stypedescender= | tr -d "\t " | tr "=" "\t" ;
showttf $1 | grep descender= | tr -d "\t " | tr "=" "\t" ;
echo ""

echo "(LineGaps should be 0)"
# captured in following grep
# showttf $1 | grep stypelinegap= | tr -d "\t " | tr "=" "\t" ;
showttf $1 | grep "linegap=" | tr -d "\t " | tr "=" "\t" ;
echo ""
echo ""
