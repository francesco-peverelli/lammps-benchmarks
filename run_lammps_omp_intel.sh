for ont in {64,128}; do
	for iter in {1..5}; do
		bcmd="env OMP_PLACES=sockets OMP_NUM_THREADS=${ont} ../src/lmp_intel_cpu_intelmpi -in $1 -pk intel 0 omp ${ont} mode mixed -sf intel"
		cmd="python3 run_wrapper.py --cmd \"$bcmd\" --bench lammps --tag $1_${ont}ont_${2}k_190p --dir \"../../../lammps/bench\" --cpu-power 1 --cpu-threshold 190"
		echo "running ${cmd}"
		eval ${cmd}
		echo "Done!"
	done
done
