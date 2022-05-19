array=( $(find -type d -regex ".*_aps") )

for dir in ${array[@]}
do
	cmd="aps --report $dir"
	echo $cmd
	$cmd
	for i in *.html; do
		mv $i ${dir}_report
	done
done

for i in *_report; do
	mv $i ${i}.html
done
