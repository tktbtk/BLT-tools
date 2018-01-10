#!/bin/bash

working_directory=`cat working_directory.cfg`
date=$0
name=$1
grep_name=$2
incident=$3
path=$working_directory"/"$date"_"$name

if [ -e $path ]; then
  echo "there is a "$path
	:
else
  mkdir $path
  echo "Created "$path
fi

if [ $input = "n" ]; then
  grep_name="n"
  break
else
  echo "grep "$grep_name
fi


endTime=`date -v+1d -j -f "%Y%m%d" $date "+%Y%m%d"`
file_path=$path"/"$date"_"$name
blt_path=$file_path".blt"
pickle_path=$file_path".pkl"
eps_path=$file_path".eps"


python2 ../../../BLT/src/bltReader/bltReader.py -v 4 -s $date -e $endTime -c route-views.linx -o $blt_path
python2 ../../../tools/incidentAnalysis/convertBltToPickel.py $blt_path
python2 ../../../tools/incidentAnalysis/draw.py $pickle_path -i $incident
if [ $grep_name != "n" ]; then
  python2 ../../../tools/incidentAnalysis/grep_AS.py $blt_path $grep_name > $file_path"_"$grep_name".blt"
  file_path=$file_path"_"$grep_name
  blt_path=$file_path".blt"
  pickle_path=$file_path".pkl"
  eps_path=$file_path".eps"
  python2 ../../../tools/incidentAnalysis/convertBltToPickel.py $blt_path
  python2 ../../../tools/incidentAnalysis/draw.py $pickle_path -i $incident
fi
