ribFilePath=$1
updateFilePath=$2
bltOutputFilePath=$3
pickleFilePath=`python2 auto/createName.py`
asNumber=$4

python2 blt.py $ribFilePath $updateFilePath -v 4 -o $bltOutputFilePath
cat $bltOutputFilePath | awk "-F|" '{if($7 ~ /'"$asNumber"'/) print $0}' > $pickleFilePath


