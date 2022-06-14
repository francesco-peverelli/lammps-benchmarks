for n in {1,2,4,8,16,32,64}; do
        for iter in {1..5}; do
		ont=1
		bcmd="mpiexec -np ${n} env OMP_NUM_THREADS=${ont} KMP_AFFINITY=granularity=fine,compact,1,0 ../bin/lmp_intel_cpu_intelmpi -in $1 -pk intel 0 omp ${ont} mode double -sf intel"
		cmd="python3 run_wrapper.py --cmd \"$bcmd\" --bench lammps --tag $1-double_${n}n_${ont}ont_${2}k_190p --dir \"../lammps/bench\" --cpu-power 0"
		echo "running ${cmd}"
		eval ${cmd}
		echo "Done!"
	done
done
