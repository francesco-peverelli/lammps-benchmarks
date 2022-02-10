for n in {1,2,4,8,16,32,64,128}; do
	ont=$((128/${n}))
	bcmd="mpiexec -np ${n} -env OMP_NUM_THREADS=${ont} ../src/lmp_intel_cpu_intelmpi -in $1 -pk intel 0 omp ${ont} mode mixed -sf intel"
	cmd="python3 run_wrapper.py --cmd \"$bcmd\" --bench lammps --tag $1_${n}n_${ont}ont_32k --dir \"../../../lammps/bench\""
	echo "running ${cmd}"
	eval ${cmd}
	echo "Done!"
done
