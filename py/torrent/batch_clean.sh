#!/bin/bash
if [[ $# -lt 1 ]]; then
  echo "Wrong # of params"
  echo "Usage:   batch_clean.sh dir prefix start_index"
  echo "         prefix use today (yyyy-MM-dd) as default"
  echo "         start_index's default is 0"
  echo "Example: batch_clean.sh /tmp AV- 0"
  echo "         batch_clean.sh /tmp"
  exit 1
fi

today=`date +%Y-%m-%d`
dir=$1/*.torrent
prefix=${2:-$today}
index=${3:-0}
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

for f in $dir; do
  python cleanser.py -i $f -o $prefix-$index -k;
  ((index+=1));
done
IFS=$SAVEIFS

echo "job done !"

