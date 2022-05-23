array=( $(find -type d -regex ".*_aps") )

for dir in ${array[@]}
do
	cmd_csv="aps-report --format csv"
	cmd="aps --report $dir"
	echo $cmd_csv
	${cmd_csv} ${dir} > ${dir}.csv
	#for i in *.html; do
	#	mv $i ${dir}_report
	#done
done

#for i in *_report; do
#	mv $i ${i}.html
#done
