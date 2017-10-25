message_path=$1
grep_word=$2
output_path=$3

cat ${message_path} | awk "-F|" '{if($7 ~ /'${grep_word}'/) print $0}' > ${output_path}
