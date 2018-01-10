#!/bin/bash

working_directory=`cat working_directory.cfg`
echo "-----------------------"
echo "Please input date of incident (ex 20171123)"
while :
do
  read input
	if [[ ${input} =~ [0-9]{8} ]]; then
		date=$input
		break
	else
		echo "This date is out of format we can parse"	
	fi
done
	

echo "Please input the name of this incident"
read input
name=$input
path=$working_directory"/"$date"_"$name


echo $path

if [ -e $path ]; then
  echo "there is a "$path
	:
else
  echo "Make a directory "$path". OK? [y/n]"
  while :
  do 
    read input
    if [ $input = y ]; then
      mkdir $path
      echo "Created "$path
      break
    elif [ $input = n ]; then
      echo "Restart please."
      exit 0
    else
      echo "please input y or n"
    fi
  done
fi

echo "Grep about AS? [n/ASN]"
while :
do 
  read input
  if [ $input = "n" ]; then
    grep_name="n"
    break
  elif [[ $input =~ [0-9]* ]]; then
    grep_name=$input
    break
  else
    echo "please input n or ASN"
  fi
done

echo "What kind of incidents is this? [ex) highjack, route_leak]"
read input
incident=$input

endTime=`date -v+1d -j -f "%Y%m%d" $date "+%Y%m%d"`
echo $endTime
file_path=$path"/"$date"_"$name
blt_path=$file_path".blt"
pickle_path=$file_path".pkl"
eps_path=$file_path".eps"


python2 ../../../BLT/src/bltReader/bltReader.py -v 4 -s $date -e $endTime -c route-views.linx -o $blt_path
python2 ../../../tools/incidentAnalysis/convertBltToPickel.py $blt_path
python2 ../../../tools/incidentAnalysis/draw.py $pickle_path -i $incident
if [ $grep_name = "n" ]; then
  exit 0
fi

python2 ../../../tools/incidentAnalysis/grep_AS.py $blt_path $grep_name > $file_path"_"$grep_name".blt"
file_path=$file_path"_"$grep_name
blt_path=$file_path".blt"
pickle_path=$file_path".pkl"
eps_path=$file_path".eps"
python2 ../../../tools/incidentAnalysis/convertBltToPickel.py $blt_path
python2 ../../../tools/incidentAnalysis/draw.py $pickle_path -i $incident
