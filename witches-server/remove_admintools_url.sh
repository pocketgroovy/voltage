URL_FILE_A=$1
URL_FILE_B=$2

sed -i -e '/#-- From here will be removed for prod --/,/#--To here will be removed for prod --/d' $URL_FILE_A
sed -i -e '/#-- From here will be removed for prod --/,/#--To here will be removed for prod --/d' $URL_FILE_B