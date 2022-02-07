
for ppn in {1,2}; do
	for n in {104,52,26}; do
		for i in {1..1}; do
			np=$((${n}/${ppn}))
			ont=$((104/${n}))
			bcmd="mpiexec.hydra -n ${np} -ppn ${ppn} env OMP_NUM_THREADS=${ont} KMP_AFFINITY=granularity=fine,compact,1,0 /opt/intel/oneapi/mkl/2022.0.2/benchmarks/hpcg/bin/xhpcg_avx2"
			cmd="python3 run_wrapper.py --cmd \"$bcmd\" --bench hpcg_cpu --tag $1x_${np}n_${ppn}ppn_${ont}ont_p220_bm2 --dir \"../\" --cpu-power 1 --cpu-threshold 90"
			echo "running ${cmd}"
			eval $cmd
			echo "Done!"
		done
	done
done
