#!/bin/bash

touch vmet.txt;
for i in `ls -1 *ttf`; do
  ~/googlefontdirectory/tools/bbox/vmet.sh $i >> vmet.txt;
done
