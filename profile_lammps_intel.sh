start_dir=$(pwd)
cd "../lammps/bench"

for n in {1,2,4,8,16,32,64}; do
#        for iter in {1..5}; do
		ont=1
		bcmd="mpiexec -aps -mps -np ${n} env OMP_NUM_THREADS=${ont} KMP_AFFINITY=granularity=fine,compact,1,0 ../src/lmp_intel_cpu_intelmpi -in $1 -pk intel 0 omp ${ont} mode double -sf intel"
		cmd="$bcmd > $start_dir/lammps/prof/$1-double_${n}n_${ont}ont_${2}k_profiling.txt"
		echo "running ${cmd}"
		eval ${cmd}
		eval "rm log.*"
		eval "mv aps_* $start_dir/lammps/prof/$1-double_${n}n_${ont}ont_${2}k_aps"
		echo "Done!"
#	done
done

for n in {1,2,4,8,16,32,64}; do
#        for iter in {1..5}; do
		ont=1
		bcmd="mpiexec -aps -mps -np ${n} env OMP_NUM_THREADS=${ont} KMP_AFFINITY=granularity=fine,compact,1,0 ../src/lmp_intel_cpu_intelmpi -in $1 -pk intel 0 omp ${ont} mode single -sf intel"
		cmd="$bcmd > $start_dir/lammps/prof/$1-single_${n}n_${ont}ont_${2}k_profiling.txt"
		echo "running ${cmd}"
		eval ${cmd}
		eval "rm log.*"
		eval "mv aps_* $start_dir/lammps/prof/$1-single_${n}n_${ont}ont_${2}k_aps"
		echo "Done!"
#	done
done
