#!/usr/bin/env bash
set -o errexit


START_DATE=$(date +"%Y-%m-%d" --date="$(date +%Y-%m-%d) last month")
END_DATE=$(date +"%Y-%m-%d")
FILE_NAME="gambit_*.csv"
FILE_COUNT=0

echo "start date $START_DATE to end date $END_DATE"
count=`ls -l $FILE_NAME | wc -l`

if [ $count -gt $FILE_COUNT ]; then
	extra_files_count=$((count-FILE_COUNT))
	oldest_file_list=`find -type f -printf '%p\n' | sort | head -n $extra_files_count`
	echo $oldest_file_list
	rm -f $oldest_file_list
fi


mysql -D gambit_en_user -u gambit_user -p913gambit -e "SELECT * FROM u_payment_history_ggl WHERE STR_TO_DATE(reg_date, '%Y-%m-%d %T') BETWEEN '$START_DATE 02' AND '$END_DATE 02'" \
| sed 's/\t/","/g;s/^/"/;s/$/"/;s/\n//g' > /home/sysdev/gambit-sales/gambit_ggl_sales_from_"$START_DATE"_to_"$END_DATE".csv

mysql -D gambit_en_user -u gambit_user -p913gambit -e "SELECT * FROM u_payment_history_app WHERE STR_TO_DATE(original_purchase_date, '%Y-%m-%dT%T') BETWEEN '$START_DATE 08' AND '$END_DATE 08'" \
| sed 's/\t/","/g;s/^/"/;s/$/"/;s/\n//g' > /home/sysdev/gambit-sales/gambit_app_sales_from_"$START_DATE"_to_"$END_DATE".csv



