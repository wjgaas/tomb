#!/bin/bash
if [[ $# -lt 1 ]]; then
  echo "Wrong # of params"
  echo "Usage:   batch_clean.sh dir prefix start_index [options]"
  echo "         prefix use today (yyyy-MM-dd) as default"
  echo "         start_index's default is 0"
  echo "Example: batch_clean.sh /tmp AV- 0"
  echo "         batch_clean.sh /tmp"
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

