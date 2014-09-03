#!/bin/bash
if [[ $# -lt 1 ]]; then
  echo "Usage:   btclean.sh input-dir output-prefix index [options]"
  echo "         output-prefix: default 'today'(yyyy-MM-dd)"
  echo "         index: default 0"
  echo "Example: btclean.sh /tmp AV- 0"
  exit 1
fi

today=`date +%Y-%m-%d`
files=$1/*.torrent; shift 1
prefix=${1:-$today}; shift 1
index=${1:-0}; shift 1

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
for f in $files; do
  cmd="./cleanser.py -i $f -o $prefix-$index $@"
  echo "$cmd"
  eval $cmd
  ((index+=1))
done
IFS=$SAVEIFS

echo "job done !"
