#for n in {1,2,4,8,16,32,64}; do
for n in {16,32}; do
	for iter in {1..5}; do
		ont=1
		bcmd="mpiexec -np ${n} env OMP_NUM_THREADS=${ont} KMP_AFFINITY=granularity=fine,compact,1,0 ../bin/lmp_intel_cpu_intelmpi -in $1 -pk intel 0 omp ${ont} mode mixed -sf intel"
		cmd="python3 run_wrapper.py --cmd \"$bcmd\" --bench lammps --tag $1_${n}n_${ont}ont_${2}k_190p --dir \"../lammps/bench\" --cpu-power 1 --cpu-threshold 120"
		echo "running ${cmd}"
		eval ${cmd}
		echo "Done!"
	done
done
