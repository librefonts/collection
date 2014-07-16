#!/bin/sh

cd $(dirname "${BASH_SOURCE[0]}")

ant lint-jar

for metadata in $(find ../../{ofl,ufl,apache} -name METADATA.json); do
  java -jar dist/lint.jar "$(dirname $metadata)"
done

cd - > /dev/null
