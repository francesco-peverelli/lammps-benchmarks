for n in {64,64}; do
	for iter in {1..5}; do
		ont=2
		bcmd="mpiexec -np ${n} env OMP_NUM_THREADS=${ont} KMP_AFFINITY=granularity=fine,compact,verbose,1,0 ../src/lmp_intel_cpu_intelmpi -in $1 -pk intel 0 omp ${ont} mode mixed -sf intel"
		cmd="python3 run_wrapper.py --cmd \"$bcmd\" --bench lammps --tag $1_${n}n_${ont}ont_${2}k_190p_testkmp --dir \"../../../lammps/bench\" --cpu-power 1 --cpu-threshold 190"
		echo "running ${cmd}"
		eval ${cmd}
		echo "Done!"
	done
done
