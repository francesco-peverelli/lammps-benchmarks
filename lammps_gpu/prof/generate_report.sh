array=( $(find -type d -regex ".*_aps") )

for dir in ${array[@]}
do
	cmd="aps --report $dir"
	echo $cmd
	$cmd
done
